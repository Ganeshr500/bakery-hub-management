"""
order_processing.py
--------------------
FUNCTIONAL MODULE 2: Order Processing
Handles placing a new customer order (validating stock, deducting
inventory, computing the bill) and cancelling an existing order
(restoring stock).
"""

from datetime import datetime
from models import Order
from storage import load_items, save_items, load_orders, save_orders
from exceptions import (
    ItemNotFoundError, InsufficientStockError, OrderNotFoundError, InvalidInputError
)
from utils import get_logger, validate_customer_name, validate_quantity

logger = get_logger(__name__)


def _next_order_id(orders: dict) -> str:
    """Generate the next sequential order ID, e.g. ORD0001, ORD0002, ..."""
    if not orders:
        return "ORD0001"
    numbers = [int(oid.replace("ORD", "")) for oid in orders if oid.startswith("ORD")]
    return f"ORD{max(numbers) + 1:04d}"


def place_order(customer_name: str, cart: dict) -> Order:
    """
    Place a new order.
    cart: dict of {item_id: quantity} requested by the customer.
    Validates stock availability for every line BEFORE deducting anything,
    so a partially-failed order never leaves inventory in an inconsistent state.
    """
    customer_name = validate_customer_name(customer_name)
    if not cart:
        raise InvalidInputError("Cannot place an order with an empty cart.")

    items = load_items()
    clean_cart = {}
    for item_id, qty in cart.items():
        item_id = item_id.strip().upper()
        qty = validate_quantity(qty)
        if item_id not in items:
            raise ItemNotFoundError(item_id)
        available = items[item_id]["stock_qty"]
        if qty > available:
            raise InsufficientStockError(item_id, qty, available)
        clean_cart[item_id] = qty

    # All lines validated -> now deduct stock and compute total
    total_amount = 0.0
    for item_id, qty in clean_cart.items():
        items[item_id]["stock_qty"] -= qty
        total_amount += items[item_id]["unit_price"] * qty
    save_items(items)

    orders = load_orders()
    order_id = _next_order_id(orders)
    order = Order(order_id, customer_name, clean_cart, round(total_amount, 2))
    orders[order_id] = order.to_dict()
    save_orders(orders)

    logger.info(f"Placed order {order_id} for {customer_name}: total {order.total_amount}")
    return order


def get_order(order_id: str) -> Order:
    order_id = order_id.strip().upper()
    orders = load_orders()
    if order_id not in orders:
        raise OrderNotFoundError(order_id)
    return Order.from_dict(orders[order_id])


def list_orders() -> list:
    """Return all orders as a list of Order objects, most recent first."""
    orders = load_orders()
    return [Order.from_dict(v) for _, v in sorted(orders.items(), reverse=True)]


def cancel_order(order_id: str) -> Order:
    """Cancel a completed order and restore the stock it consumed."""
    order_id = order_id.strip().upper()
    orders = load_orders()
    if order_id not in orders:
        raise OrderNotFoundError(order_id)

    order_data = orders[order_id]
    if order_data["status"] == "CANCELLED":
        raise InvalidInputError(f"Order '{order_id}' is already cancelled.")

    items = load_items()
    for item_id, qty in order_data["line_items"].items():
        if item_id in items:
            items[item_id]["stock_qty"] += qty
    save_items(items)

    order_data["status"] = "CANCELLED"
    save_orders(orders)
    logger.info(f"Cancelled order {order_id}, stock restored")
    return Order.from_dict(order_data)
