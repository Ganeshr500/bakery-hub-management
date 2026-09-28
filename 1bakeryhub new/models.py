"""
models.py
---------
Defines the core data classes: BakeryItem and Order. Each knows how to
convert to/from a plain dict (needed because JSON can only store plain
data types).
"""

from datetime import datetime


class BakeryItem:
    """Represents one product sold by the bakery (e.g. a loaf of bread)."""

    def __init__(self, item_id, name, category, unit_price, stock_qty, reorder_level=10):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.unit_price = unit_price
        self.stock_qty = stock_qty
        self.reorder_level = reorder_level

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "category": self.category,
            "unit_price": self.unit_price,
            "stock_qty": self.stock_qty,
            "reorder_level": self.reorder_level,
        }

    @staticmethod
    def from_dict(data: dict) -> "BakeryItem":
        return BakeryItem(
            item_id=data["item_id"],
            name=data["name"],
            category=data["category"],
            unit_price=data["unit_price"],
            stock_qty=data["stock_qty"],
            reorder_level=data.get("reorder_level", 10),
        )

    def is_low_stock(self) -> bool:
        return self.stock_qty <= self.reorder_level

    def __repr__(self):
        return f"BakeryItem({self.item_id}, {self.name}, stock={self.stock_qty})"


class Order:
    """Represents one customer order: a set of items, quantities, and totals."""

    def __init__(self, order_id, customer_name, line_items, total_amount,
                 timestamp=None, status="COMPLETED"):
        self.order_id = order_id
        self.customer_name = customer_name
        self.line_items = line_items          # dict: item_id -> qty
        self.total_amount = total_amount
        self.timestamp = timestamp or datetime.now().isoformat(timespec="seconds")
        self.status = status                   # "COMPLETED" or "CANCELLED"

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "line_items": self.line_items,
            "total_amount": self.total_amount,
            "timestamp": self.timestamp,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "Order":
        return Order(
            order_id=data["order_id"],
            customer_name=data["customer_name"],
            line_items=data["line_items"],
            total_amount=data["total_amount"],
            timestamp=data.get("timestamp"),
            status=data.get("status", "COMPLETED"),
        )

    def __repr__(self):
        return f"Order({self.order_id}, {self.customer_name}, {self.status})"
