import unittest
from unittest.mock import Mock
from order_service import (
    Order,
    InventoryService,
    PaymentGateway,
    InventoryShortageError,
    PaymentFailedError,
    InvalidOrderError
)

class TestOrderService(unittest.TestCase):
    def setUp(self):
        # Create mocks for external dependencies
        self.mock_inventory = Mock(spec=InventoryService)
        self.mock_payment = Mock(spec=PaymentGateway)
        # Create common test order
        self.order = Order(
            inventory_service=self.mock_inventory,
            payment_gateway=self.mock_payment,
            customer_email="customer@example.com"
        )

    def test_add_item_success(self):
        """Test adding items to the order successfully."""
        self.order.add_item("item-1", 10.0, 2)
        self.assertIn("item-1", self.order.items)
        self.assertEqual(self.order.items["item-1"]["price"], 10.0)
        self.assertEqual(self.order.items["item-1"]["qty"], 2)

    def test_add_duplicate_item_increments_quantity(self):
        """Test that adding duplicate items updates the quantity correctly."""
        self.order.add_item("item-1", 10.0, 2)
        self.order.add_item("item-1", 10.0, 3)
        self.assertEqual(self.order.items["item-1"]["qty"], 5)

    def test_add_item_negative_price(self):
        """Test that adding an item with a negative price raises ValueError."""
        with self.assertRaises(ValueError):
            self.order.add_item("item-1", -5.0, 1)

    def test_add_item_invalid_quantity(self):
        """Test that adding an item with zero or negative quantity raises ValueError."""
        with self.assertRaises(ValueError):
            self.order.add_item("item-1", 10.0, 0)
        with self.assertRaises(ValueError):
            self.order.add_item("item-1", 10.0, -1)

    def test_remove_item(self):
        """Test removing an item from the cart."""
        self.order.add_item("item-1", 10.0, 2)
        self.order.remove_item("item-1")
        self.assertNotIn("item-1", self.order.items)

    def test_remove_nonexistent_item_does_not_fail(self):
        """Test that removing an item that isn't in the cart passes silently."""
        self.order.remove_item("non-existent")
        self.assertNotIn("non-existent", self.order.items)

    def test_total_price(self):
        """Test that the total price calculates correctly."""
        self.order.add_item("item-1", 10.5, 2) # 21.0
        self.order.add_item("item-2", 5.0, 3)  # 15.0
        self.assertEqual(self.order.total_price, 36.0)

    def test_apply_discount_regular_no_discount(self):
        """Test that regular customers get no discount if total <= 100."""
        self.order.add_item("item-1", 50.0, 2) # 100.00 total
        self.assertEqual(self.order.apply_discount(), 100.0)

    def test_apply_discount_regular_with_discount(self):
        """Test that regular customers get 10% off if total > 100."""
        self.order.add_item("item-1", 60.0, 2) # 120.00 total
        self.assertEqual(self.order.apply_discount(), 108.0) # 120 * 0.9 = 108.0

    def test_apply_discount_vip(self):
        """Test that VIP customers get 20% off flat."""
        vip_order = Order(
            inventory_service=self.mock_inventory,
            payment_gateway=self.mock_payment,
            customer_email="vip@example.com",
            is_vip=True
        )
        vip_order.add_item("item-1", 50.0, 1) # 50.00 total
        self.assertEqual(vip_order.apply_discount(), 40.0) # 50 * 0.8 = 40.0

    def test_checkout_empty_cart_raises_error(self):
        """Test checking out an empty cart raises InvalidOrderError."""
        with self.assertRaises(InvalidOrderError):
            self.order.checkout()

    def test_checkout_inventory_shortage(self):
        """Test that insufficient inventory raises InventoryShortageError."""
        self.order.add_item("item-1", 10.0, 5)
        # Mock inventory to report stock of 4
        self.mock_inventory.get_stock.return_value = 4
        
        with self.assertRaises(InventoryShortageError):
            self.order.checkout()
        
        self.mock_inventory.get_stock.assert_called_once_with("item-1")
        self.mock_payment.charge.assert_not_called()

    def test_checkout_payment_declined(self):
        """Test that a payment transaction decline raises PaymentFailedError."""
        self.order.add_item("item-1", 10.0, 2) # 20.00 total
        
        self.mock_inventory.get_stock.return_value = 10
        self.mock_payment.charge.return_value = False
        
        with self.assertRaises(PaymentFailedError) as context:
            self.order.checkout()
            
        self.assertIn("Transaction declined by gateway", str(context.exception))
        self.mock_payment.charge.assert_called_once_with(20.0, "USD")
        self.mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_payment_gateway_exception(self):
        """Test that payment gateway network issues raise PaymentFailedError."""
        self.order.add_item("item-1", 10.0, 2)
        
        self.mock_inventory.get_stock.return_value = 10
        self.mock_payment.charge.side_effect = Exception("Connection Timeout")
        
        with self.assertRaises(PaymentFailedError) as context:
            self.order.checkout()
            
        self.assertIn("Connection Timeout", str(context.exception))
        self.mock_inventory.decrement_stock.assert_not_called()

    def test_checkout_success(self):
        """Test a fully successful checkout path."""
        self.order.add_item("item-1", 20.0, 3) # 60.00 total
        self.order.add_item("item-2", 15.0, 4) # 60.00 total
        # Raw total = 120.00 -> regular discount (10%) -> final = 108.00
        
        self.mock_inventory.get_stock.side_effect = lambda prod_id: 10
        self.mock_payment.charge.return_value = True
        
        result = self.order.checkout()
        
        # Verify status and is_paid
        self.assertTrue(self.order.is_paid)
        self.assertEqual(self.order.status, "COMPLETED")
        self.assertEqual(result, {"status": "success", "charged_amount": 108.0})
        
        # Verify correct calls to payment gateway
        self.mock_payment.charge.assert_called_once_with(108.0, "USD")
        
        # Verify inventory decrement calls
        self.assertEqual(self.mock_inventory.decrement_stock.call_count, 2)
        self.mock_inventory.decrement_stock.assert_any_call("item-1", 3)
        self.mock_inventory.decrement_stock.assert_any_call("item-2", 4)
