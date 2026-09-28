# BakeryHub — Bakery Inventory, Orders & Sales Analytics System

## Overview
BakeryHub is a menu-driven, console-based Python application built for the
first-semester Python course project. It helps a small bakery track what
products it has in stock, process customer orders (deducting stock and
computing bills automatically), and generate simple sales reports — backed
by a real SQLite database (`data/bakeryhub.db`) instead of flat JSON files.

## Features
- **Inventory Management (CRUD):** add, view, update the price of, restock,
  and delete bakery items (bread, cakes, pastries, cookies, beverages).
- **Order Processing:** place a multi-item order for a customer, with stock
  checked *before* anything is deducted (so a failed order never leaves
  inventory half-updated); cancel an order to automatically restore stock.
- **Reports & Analytics:** a low-stock alert report, a total revenue /
  average order value summary, and a best-selling items ranking.
- Persistent storage in a SQLite database (`data/bakeryhub.db`), with an
  `items` table and an `orders` table. Data from an older JSON-based run
  (`data/items.json` / `data/orders.json`) is imported automatically the
  first time the database is used.
- Centralized logging of every operation to `logs/app.log`.
- Custom exception hierarchy for clean, predictable error handling.
- Unit-tested core logic (16 tests, `tests/test_bakeryhub.py`).

## Technologies / Tools Used
- **Language:** Python 3
- **Standard library only:** `sqlite3`, `json`, `logging`, `re`, `unittest`, `os`, `datetime`
- **Storage:** SQLite database (`data/bakeryhub.db`)
- **Version control:** Git

## Project Structure
```
bakeryhub/
├── main.py                  # CLI entry point / menu (Presentation layer)
├── inventory_manager.py      # Module 1: CRUD for bakery items
├── order_processing.py        # Module 2: place/cancel orders, stock handling
├── reports.py                   # Module 3: low-stock, revenue, best-sellers
├── models.py                      # BakeryItem & Order data classes (OOP)
├── database.py                      # SQLite connection + schema
├── storage.py                         # Persistence layer (items + orders), backed by database.py
├── utils.py                              # Logging setup + input validation
├── exceptions.py                           # Custom exception classes
├── config.py                                 # Constants & file paths
├── tests/
│   └── test_bakeryhub.py                       # Unit tests (unittest)
├── diagrams/
│   └── make_diagrams.py                           # Script that builds design diagrams
├── data/                                             # bakeryhub.db (created at runtime)
├── logs/                                               # app.log (created at runtime)
├── statement.md
└── README.md
```

## Steps to Install & Run
1. Ensure Python 3.8+ is installed:
   ```bash
   python3 --version
   ```
2. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd bakeryhub
   ```
3. No external dependencies are required to run the app (standard library
   only). Run it directly:
   ```bash
   python3 main.py
   ```
4. Follow the on-screen menu to add items, place orders, and view reports.

## Instructions for Testing
Run the unit test suite from the project root:
```bash
python -m unittest tests/test_bakeryhub.py -v
```
All 16 tests should pass. Tests use a separate temporary SQLite database
(`data/bakeryhub_test.db`) so your real inventory and order data are never
affected.

## Regenerating the Design Diagrams
The report's diagrams are generated with matplotlib (no network/tools needed):
```bash
pip install matplotlib
python3 diagrams/make_diagrams.py
```

## Screenshots
See the attached project report (PDF) for sample console output: adding
items, placing an order, and generated reports.

## Author
Prepared as part of the VITyarthi "Build Your Own Project" submission —
Python (First Semester).
