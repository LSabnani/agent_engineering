#  Mock Test is a collection of unit tests that could be applied to an online order service.
# This is a simple Order service that has the following key functionality in the checkout function:

Validates cart is not empty. Does not allow negative or zero order quantity
Check stock for all items. Validates if item is valid, qty is available vs stock
Calculates final price. Applies discounts based on customer profile, order qty and price
Charges payment. Verifies the transaction for the card payment
Updates inventory.