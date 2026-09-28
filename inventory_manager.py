"""
inventory_manager.py
---------------------
FUNCTIONAL MODULE 1: Inventory Management
Provides Create, Read, Update, Delete (CRUD) operations on bakery item
records, plus restocking.
"""

from config import DEFAULT_REORDER_LEVEL
from models import BakeryItem
from storage import load_items, save_items
from exceptions import ItemNotFoundError, DuplicateItemError
from utils import (
    get_logger, validate_item_id, validate_item_name,
    validate_category, validate_price, validate_quantity,
)

logger = get_logger(__name__)


def add_item(item_id, name, category, unit_price, stock_qty, reorder_level=DEFAULT_REORDER_LEVEL) -> BakeryItem:
    """Create a new bakery item. Raises DuplicateItemError if it already exists."""
    item_id = validate_item_id(item_id)
    name = validate_item_name(name)
    category = validate_category(category)
    unit_price = validate_price(unit_price)
    stock_qty = validate_quantity(stock_qty, allow_zero=True)

    items = load_items()
    if item_id in items:
        raise DuplicateItemError(item_id)

    item = BakeryItem(item_id, name, category, unit_price, stock_qty, reorder_level)
    items[item_id] = item.to_dict()
    save_items(items)
    logger.info(f"Added item {item_id} - {name} ({stock_qty} units @ {unit_price})")
    return item


def get_item(item_id: str) -> BakeryItem:
    """Read a single item's full record."""
    item_id = item_id.strip().upper()
    items = load_items()
    if item_id not in items:
        raise ItemNotFoundError(item_id)
    return BakeryItem.from_dict(items[item_id])


def list_items() -> list:
    """Return all items as a list of BakeryItem objects, sorted by item_id."""
    items = load_items()
    return [BakeryItem.from_dict(v) for _, v in sorted(items.items())]


def update_item_price(item_id: str, new_price) -> BakeryItem:
    """Update an existing item's unit price."""
    item_id = item_id.strip().upper()
    new_price = validate_price(new_price)

    items = load_items()
    if item_id not in items:
        raise ItemNotFoundError(item_id)

    items[item_id]["unit_price"] = new_price
    save_items(items)
    logger.info(f"Updated price for {item_id} -> {new_price}")
    return BakeryItem.from_dict(items[item_id])


def restock_item(item_id: str, additional_qty) -> BakeryItem:
    """Increase an item's stock quantity (e.g. after a fresh baking batch)."""
    item_id = item_id.strip().upper()
    additional_qty = validate_quantity(additional_qty)

    items = load_items()
    if item_id not in items:
        raise ItemNotFoundError(item_id)

    items[item_id]["stock_qty"] += additional_qty
    save_items(items)
    logger.info(f"Restocked {item_id} by {additional_qty} units")
    return BakeryItem.from_dict(items[item_id])


def delete_item(item_id: str) -> None:
    """Delete an item record permanently."""
    item_id = item_id.strip().upper()
    items = load_items()
    if item_id not in items:
        raise ItemNotFoundError(item_id)

    del items[item_id]
    save_items(items)
    logger.info(f"Deleted item {item_id}")
