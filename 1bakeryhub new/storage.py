"""
storage.py
----------
Handles all reading/writing of bakery data (items and orders). Persistence
now lives in a real SQLite database (data/bakeryhub.db, see database.py)
instead of flat JSON files, so inventory and orders are tracked as proper
database rows -- and can be inspected/queried directly with any SQLite
tool if needed.

The public interface is unchanged on purpose: load_items()/save_items()/
load_orders()/save_orders() still take and return plain dicts keyed by id,
exactly as before. That means inventory_manager.py, order_processing.py,
reports.py, and main.py did not need to change at all -- only the storage
layer underneath them did.

On first use, if the database has no items/orders yet but legacy
items.json / orders.json files exist (from a previous JSON-based run),
their data is imported automatically so nobody loses existing inventory
just from upgrading.
"""

import json
import os
import sqlite3

import config
from database import get_connection
from exceptions import StorageError
from utils import get_logger

logger = get_logger(__name__)


def _load_legacy_json(path: str) -> dict:
    """Best-effort read of an old JSON data file. Returns {} if the file
    doesn't exist or can't be parsed -- migration is a convenience, not a
    hard requirement."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"Could not read legacy data file {path}: {e}")
        return {}


def _migrate_legacy_data_if_needed() -> None:
    """One-time import of pre-existing items.json / orders.json into the
    database. Only runs when the corresponding table is still empty, so it
    never overwrites real database data with stale JSON data."""
    conn = get_connection()
    try:
        item_count = conn.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        if item_count == 0:
            legacy_items = _load_legacy_json(config.ITEMS_FILE)
            if legacy_items:
                conn.executemany(
                    "INSERT OR REPLACE INTO items "
                    "(item_id, name, category, unit_price, stock_qty, reorder_level) "
                    "VALUES (:item_id, :name, :category, :unit_price, :stock_qty, :reorder_level)",
                    [
                        {**data, "item_id": item_id, "reorder_level": data.get("reorder_level", 10)}
                        for item_id, data in legacy_items.items()
                    ],
                )
                logger.info(f"Migrated {len(legacy_items)} item(s) from {config.ITEMS_FILE} into the database")

        order_count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        if order_count == 0:
            legacy_orders = _load_legacy_json(config.ORDERS_FILE)
            if legacy_orders:
                conn.executemany(
                    "INSERT OR REPLACE INTO orders "
                    "(order_id, customer_name, line_items, total_amount, timestamp, status) "
                    "VALUES (:order_id, :customer_name, :line_items, :total_amount, :timestamp, :status)",
                    [
                        {
                            "order_id": order_id,
                            "customer_name": data["customer_name"],
                            "line_items": json.dumps(data["line_items"]),
                            "total_amount": data["total_amount"],
                            "timestamp": data["timestamp"],
                            "status": data.get("status", "COMPLETED"),
                        }
                        for order_id, data in legacy_orders.items()
                    ],
                )
                logger.info(f"Migrated {len(legacy_orders)} order(s) from {config.ORDERS_FILE} into the database")

        conn.commit()
    finally:
        conn.close()


def load_items() -> dict:
    """Load all bakery item records, keyed by item_id."""
    try:
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM items").fetchall()
            return {row["item_id"]: dict(row) for row in rows}
        finally:
            conn.close()
    except sqlite3.Error as e:
        logger.error(f"Failed to load items from the database: {e}")
        raise StorageError(f"Could not read items from the database: {e}")


def save_items(items: dict) -> None:
    """Persist the given dict of item records (replaces the whole table,
    mirroring the old JSON behaviour of overwriting the full file)."""
    try:
        conn = get_connection()
        try:
            conn.execute("DELETE FROM items")
            if items:
                conn.executemany(
                    "INSERT INTO items "
                    "(item_id, name, category, unit_price, stock_qty, reorder_level) "
                    "VALUES (:item_id, :name, :category, :unit_price, :stock_qty, :reorder_level)",
                    list(items.values()),
                )
            conn.commit()
            logger.info(f"Saved {len(items)} record(s) to the database (items)")
        finally:
            conn.close()
    except sqlite3.Error as e:
        logger.error(f"Failed to save items to the database: {e}")
        raise StorageError(f"Could not write items to the database: {e}")


def load_orders() -> dict:
    """Load all order records, keyed by order_id."""
    try:
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM orders").fetchall()
            result = {}
            for row in rows:
                data = dict(row)
                data["line_items"] = json.loads(data["line_items"])
                result[row["order_id"]] = data
            return result
        finally:
            conn.close()
    except sqlite3.Error as e:
        logger.error(f"Failed to load orders from the database: {e}")
        raise StorageError(f"Could not read orders from the database: {e}")


def save_orders(orders: dict) -> None:
    """Persist the given dict of order records (replaces the whole table)."""
    try:
        conn = get_connection()
        try:
            conn.execute("DELETE FROM orders")
            if orders:
                rows = []
                for data in orders.values():
                    row = dict(data)
                    row["line_items"] = json.dumps(data["line_items"])
                    rows.append(row)
                conn.executemany(
                    "INSERT INTO orders "
                    "(order_id, customer_name, line_items, total_amount, timestamp, status) "
                    "VALUES (:order_id, :customer_name, :line_items, :total_amount, :timestamp, :status)",
                    rows,
                )
            conn.commit()
            logger.info(f"Saved {len(orders)} record(s) to the database (orders)")
        finally:
            conn.close()
    except sqlite3.Error as e:
        logger.error(f"Failed to save orders to the database: {e}")
        raise StorageError(f"Could not write orders to the database: {e}")


# Run once, the moment this module is first imported: pull in any data
# left over from a previous JSON-based version of BakeryHub.
_migrate_legacy_data_if_needed()
