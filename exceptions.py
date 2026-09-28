"""
exceptions.py
-------------
Custom exception classes used across the BakeryHub application.
Keeping these separate makes error handling explicit and easy to maintain.
"""


class BakeryHubError(Exception):
    """Base class for all application-specific errors."""
    pass


class ItemNotFoundError(BakeryHubError):
    """Raised when a lookup is made for an item_id that does not exist."""
    def __init__(self, item_id):
        super().__init__(f"No bakery item found with ID '{item_id}'.")
        self.item_id = item_id


class DuplicateItemError(BakeryHubError):
    """Raised when trying to add an item whose item_id already exists."""
    def __init__(self, item_id):
        super().__init__(f"An item with ID '{item_id}' already exists.")
        self.item_id = item_id


class InsufficientStockError(BakeryHubError):
    """Raised when an order requests more units than are currently in stock."""
    def __init__(self, item_id, requested, available):
        super().__init__(
            f"Insufficient stock for '{item_id}': requested {requested}, only {available} available."
        )
        self.item_id = item_id
        self.requested = requested
        self.available = available


class OrderNotFoundError(BakeryHubError):
    """Raised when a lookup is made for an order_id that does not exist."""
    def __init__(self, order_id):
        super().__init__(f"No order found with ID '{order_id}'.")
        self.order_id = order_id


class InvalidInputError(BakeryHubError):
    """Raised when user-supplied data fails validation."""
    pass


class StorageError(BakeryHubError):
    """Raised when reading from or writing to a JSON data file fails."""
    pass
