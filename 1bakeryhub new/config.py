"""
config.py
---------
Central place for constants and file paths so nothing is hard-coded
throughout the codebase. Change values here to reconfigure the app.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

ITEMS_FILE = os.path.join(DATA_DIR, "items.json")
ITEMS_BACKUP_FILE = os.path.join(DATA_DIR, "items_backup.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
ORDERS_BACKUP_FILE = os.path.join(DATA_DIR, "orders_backup.json")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# SQLite database that now backs all inventory + order storage. The old
# ITEMS_FILE/ORDERS_FILE JSON paths above are kept only so that any data
# from a previous JSON-based run can be auto-imported the first time the
# database is used (see storage.py).
DB_FILE = os.path.join(DATA_DIR, "bakeryhub.db")

# Item categories tracked by the bakery
CATEGORIES = ["Bread", "Cake", "Pastry", "Cookie", "Beverage"]

# If stock falls at or below this number, the item shows up in the low-stock report
DEFAULT_REORDER_LEVEL = 10

MAX_UNIT_PRICE = 5000.0   # sanity ceiling for a single item's price (local currency)
MAX_ORDER_QTY = 500        # sanity ceiling for quantity in a single order line

# Ensure required folders exist the moment config is imported
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
