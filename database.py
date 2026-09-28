"""
database.py
------------
Owns the SQLite database that stores BakeryHub's inventory and order data
(data/bakeryhub.db). This is the only module that talks SQL directly:
storage.py calls get_connection() and runs plain queries against the
`items` and `orders` tables, and everything above storage.py (inventory
manager, order processing, reports, main) never has to know a database is
involved at all.

Using `config.DB_FILE` (attribute access) rather than importing the name
directly means the path can still be swapped out at runtime -- which is
exactly what tests/test_bakeryhub.py does to keep test data isolated from
real bakery data.
"""

import sqlite3

import config


def get_connection() -> sqlite3.Connection:
    """Open a connection to the BakeryHub database, creating the schema
    on first use. Callers are responsible for closing the connection
    (and committing, for writes) -- storage.py does this for every call."""
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row
    _ensure_schema(conn)
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS items (
            item_id       TEXT PRIMARY KEY,
            name          TEXT NOT NULL,
            category      TEXT NOT NULL,
            unit_price    REAL NOT NULL,
            stock_qty     INTEGER NOT NULL,
            reorder_level INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id      TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            line_items    TEXT NOT NULL,   -- JSON object: {"item_id": qty, ...}
            total_amount  REAL NOT NULL,
            timestamp     TEXT NOT NULL,
            status        TEXT NOT NULL
        );
        """
    )
    conn.commit()
