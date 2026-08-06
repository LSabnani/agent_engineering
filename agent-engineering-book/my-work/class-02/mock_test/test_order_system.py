import unittest
from unittest.mock import Mock, call

from order_system import (
    Order,
    InventoryService,
    PaymentGateway,
    InventoryShortageError,
    PaymentFailedError,
    InvalidOrderError,
)

class TestCartManagement(unittest.TestCase):
    def setUp(self):
        self.mock_inventory = Mock(spec=InventoryService)
        self.mock_payment = Mock(spec=PaymentGateway)
        self.order = Order(
            inventory_service=self.mock_inventory,
            payment_gateway=self.mock_payment,
            customer_email="alice@example.com",
            is_vip=False,
        )

    def test_add_item_success(self):
        self.order.add_item("item_1", 25.0, 2)
        self.assertEqual(self.order.items, {"item_1": {"price": 25.0, "qty": 2}})

    def test_add_item_increment_quantity(self):
        self.order.add_item("item_1", 25.0, 2)
        self.order.add_item("item_1", 25.0, 3)
        self.assertEqual(self.order.items["item_1"]["qty"], 5)

    def test_add_item_negative_price(self):
        with self.assertRaisesRegex(ValueError, "Price cannot be negative"):
            self.order.add_item("item_1", -10.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be greater than zero"):
            self.order.add_item("item_1", 10.0, 0)

        with self.assertRaisesRegex(ValueError, "Quantity must be greater than zero"):
            self.order.add_item("item_1", 10.0, -5)

    def test_remove_item_existing(self):
        self.order.add_item("item_1", 25.0, 2)
        self.order.add_item("item_2", 15.0, 1)
        self.order.remove_item("item_1")
        self.assertNotIn("item_1", self.order.items)
        self.assertIn("item_2", self.order.items)

    def test_remove_item_non_existing(self):
        self.order.add_item("item_1", 25.0, 1)
        self.order.remove_item("non_existent_item")
        self.assertIn("item_1", self.order.items)


class TestDiscountCalculation(unittest.TestCase):
    def setUp(self):
        self.mock_inventory = Mock(spec=InventoryService)
        self.mock_payment = Mock(spec=PaymentGateway)
        self.regular_order = Order(
            inventory_service=self.mock_inventory,
            payment_gateway=self.mock_payment,
            customer_email="alice@example.com",
            is_vip=False,
        )
        self.vip_order = Order(
            inventory_service=self.mock_inventory,
            payment_gateway=self.mock_payment,
            customer_email="bob@example.com",
            is_vip=True,
        )

    def test_total_price(self):
        self.assertEqual(self.regular_order.total_price, 0.0)
        self.regular_order.add_item("item_1", 20.0, 2)  # 40.0
        self.regular_order.add_item("item_2", 15.5, 3)  # 46.5
        self.assertEqual(self.regular_order.total_price, 86.5)

    def test_discount_regular_under_100(self):
        self.regular_order.add_item("item_1", 50.0, 1)
        self.assertEqual(self.regular_order.apply_discount(), 50.0)

    def test_discount_regular_exactly_100(self):
        self.regular_order.add_item("item_1", 100.0, 1)
        self.assertEqual(self.regular_order.apply_discount(), 100.0)

    def test_discount_regular_over_100(self):
        self.regular_order.add_item("item_1", 150.0, 1)
        self.assertEqual(self.regular_order.apply_discount(), 135.0)

    def test_discount_vip_under_100(self):
        self.vip_order.add_item("item_1", 50.0, 1)
        self.assertEqual(self.vip_order.apply_discount(), 40.0)

    def test_discount_vip_over_100(self):
        self.vip_order.add_item("item_1", 200.0, 1)
        self.assertEqual(self.vip_order.apply_discount(), 160.0)


class TestCheckoutFlow(unittest.TestCase):
    def setUp(self):
        self.mock_inventory = Mock(spec=InventoryService)
        self.mock_payment = Mock(spec=PaymentGateway)
        self.order = Order(
            inventory_service=self.mock_inventory,
            payment_gateway=self.mock_payment,
            customer_email="alice@example.com",
            is_vip=False,
        )
        self.vip_order = Order(
            inventory_service=self.mock_inventory,
            payment_gateway=self.mock_payment,
            customer_email="bob@example.com",
            is_vip=True,
        )

    def test_checkout_empty_cart(self):
        with self.assertRaisesRegex(InvalidOrderError, "Cannot checkout an empty cart"):
            self.order.checkout()

    def test_checkout_inventory_shortage(self):
        self.order.add_item("item_1", 50.0, 5)
        self.mock_inventory.get_stock.return_value = 3

        with self.assertRaisesRegex(InventoryShortageError, "Not enough stock for item_1"):
            self.order.checkout()

        self.mock_inventory.get_stock.assert_called_once_with("item_1")
        self.mock_payment.charge.assert_not_called()
        self.mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_payment_declined(self):
        self.order.add_item("item_1", 50.0, 1)
        self.mock_inventory.get_stock.return_value = 10
        self.mock_payment.charge.return_value = False

        with self.assertRaisesRegex(PaymentFailedError, "Payment gateway error: Transaction declined by gateway"):
            self.order.checkout()

        self.mock_inventory.get_stock.assert_called_once_with("item_1")
        self.mock_payment.charge.assert_called_once_with(50.0, "USD")
        self.mock_inventory.decrement_stock.assert_not_called()
        self.assertFalse(self.order.is_paid)
        self.assertEqual(self.order.status, "DRAFT")

    def test_checkout_payment_gateway_exception(self):
        self.order.add_item("item_1", 50.0, 1)
        self.mock_inventory.get_stock.return_value = 10
        self.mock_payment.charge.side_effect = TimeoutError("Connection timed out")

        with self.assertRaisesRegex(PaymentFailedError, "Payment gateway error: Connection timed out"):
            self.order.checkout()

        self.mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_success(self):
        self.vip_order.add_item("prod_A", 100.0, 2)  # Total 200 -> VIP 20% off -> 160.0
        self.vip_order.add_item("prod_B", 50.0, 1)   # Total 250 -> VIP 20% off -> 200.0

        self.mock_inventory.get_stock.side_effect = lambda prod_id: {"prod_A": 10, "prod_B": 5}[prod_id]
        self.mock_payment.charge.return_value = True

        result = self.vip_order.checkout()

        self.mock_inventory.get_stock.assert_has_calls([call("prod_A"), call("prod_B")], any_order=True)
        self.mock_payment.charge.assert_called_once_with(200.0, "USD")
        self.mock_inventory.decrement_stock.assert_has_calls([call("prod_A", 2), call("prod_B", 1)], any_order=True)

        self.assertTrue(self.vip_order.is_paid)
        self.assertEqual(self.vip_order.status, "COMPLETED")
        self.assertEqual(result, {"status": "success", "charged_amount": 200.0})


class TestInterfaceContracts(unittest.TestCase):
    def test_inventory_service_raises_not_implemented(self):
        service = InventoryService()
        with self.assertRaises(NotImplementedError):
            service.get_stock("p1")
        with self.assertRaises(NotImplementedError):
            service.decrement_stock("p1", 1)

    def test_payment_gateway_raises_not_implemented(self):
        gateway = PaymentGateway()
        with self.assertRaises(NotImplementedError):
            gateway.charge(100.0, "USD")


if __name__ == "__main__":
    unittest.main()
