"""
tests/test_bakeryhub.py
------------------------
Unit tests covering all three functional modules. Run with:
    python -m unittest tests/test_bakeryhub.py -v

Uses temporary data files so tests never touch real bakery data.
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

# Redirect storage to a throwaway test database BEFORE importing modules
# that use it, so tests never touch real bakery data. TEST_ITEMS_FILE /
# TEST_ORDERS_FILE point at JSON files that never exist, which just keeps
# storage.py's legacy-JSON migration from importing anything during tests.
TEST_DB_FILE = os.path.join(config.DATA_DIR, "bakeryhub_test.db")
TEST_ITEMS_FILE = os.path.join(config.DATA_DIR, "items_test.json")
TEST_ORDERS_FILE = os.path.join(config.DATA_DIR, "orders_test.json")
config.DB_FILE = TEST_DB_FILE
config.ITEMS_FILE = TEST_ITEMS_FILE
config.ORDERS_FILE = TEST_ORDERS_FILE

import inventory_manager as im
import order_processing as op
import reports as rp
from exceptions import (
    ItemNotFoundError, DuplicateItemError, InsufficientStockError,
    InvalidInputError, OrderNotFoundError,
)


def _clean():
    # Deleting the database file wipes both tables; storage.py recreates
    # the schema automatically the next time a connection is opened.
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)


class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        _clean()

    def tearDown(self):
        _clean()

    def test_add_and_get_item(self):
        im.add_item("br001", "White Bread", "Bread", 40, 50)
        item = im.get_item("BR001")
        self.assertEqual(item.name, "White Bread")
        self.assertEqual(item.stock_qty, 50)

    def test_duplicate_item_rejected(self):
        im.add_item("br002", "Brown Bread", "Bread", 45, 30)
        with self.assertRaises(DuplicateItemError):
            im.add_item("br002", "Something Else", "Bread", 50, 10)

    def test_get_missing_item_raises(self):
        with self.assertRaises(ItemNotFoundError):
            im.get_item("NOPE1")

    def test_invalid_category_rejected(self):
        with self.assertRaises(InvalidInputError):
            im.add_item("ck001", "Choc Cookie", "Snacks", 20, 40)  # invalid category

    def test_restock_and_update_price(self):
        im.add_item("cake01", "Chocolate Cake", "Cake", 300, 5)
        im.restock_item("cake01", 10)
        item = im.get_item("cake01")
        self.assertEqual(item.stock_qty, 15)
        im.update_item_price("cake01", 350)
        self.assertEqual(im.get_item("cake01").unit_price, 350)

    def test_low_stock_flag(self):
        im.add_item("pas01", "Croissant", "Pastry", 60, 5, reorder_level=10)
        item = im.get_item("pas01")
        self.assertTrue(item.is_low_stock())

    def test_delete_item(self):
        im.add_item("del01", "Temp Item", "Cookie", 10, 5)
        im.delete_item("del01")
        with self.assertRaises(ItemNotFoundError):
            im.get_item("del01")


class TestOrderProcessing(unittest.TestCase):
    def setUp(self):
        _clean()
        im.add_item("br001", "White Bread", "Bread", 40, 50)
        im.add_item("cake01", "Chocolate Cake", "Cake", 300, 5)

    def tearDown(self):
        _clean()

    def test_place_order_deducts_stock_and_computes_total(self):
        order = op.place_order("Asha", {"br001": 2, "cake01": 1})
        self.assertEqual(order.total_amount, 380.0)  # 2*40 + 1*300
        self.assertEqual(im.get_item("br001").stock_qty, 48)
        self.assertEqual(im.get_item("cake01").stock_qty, 4)

    def test_insufficient_stock_rejected_and_no_partial_deduction(self):
        with self.assertRaises(InsufficientStockError):
            op.place_order("Rahul", {"br001": 2, "cake01": 100})
        # br001 stock must be untouched since the whole order was rejected
        self.assertEqual(im.get_item("br001").stock_qty, 50)

    def test_unknown_item_in_cart_rejected(self):
        with self.assertRaises(ItemNotFoundError):
            op.place_order("Neha", {"ZZZ99": 1})

    def test_cancel_order_restores_stock(self):
        order = op.place_order("Vikram", {"br001": 3})
        self.assertEqual(im.get_item("br001").stock_qty, 47)
        op.cancel_order(order.order_id)
        self.assertEqual(im.get_item("br001").stock_qty, 50)
        self.assertEqual(op.get_order(order.order_id).status, "CANCELLED")

    def test_cancel_missing_order_raises(self):
        with self.assertRaises(OrderNotFoundError):
            op.cancel_order("ORD9999")

    def test_empty_cart_rejected(self):
        with self.assertRaises(InvalidInputError):
            op.place_order("Empty Cart", {})


class TestReports(unittest.TestCase):
    def setUp(self):
        _clean()
        im.add_item("br001", "White Bread", "Bread", 40, 3, reorder_level=10)  # low stock
        im.add_item("cake01", "Chocolate Cake", "Cake", 300, 20, reorder_level=5)
        op.place_order("Asha", {"br001": 2})
        op.place_order("Rahul", {"cake01": 1, "br001": 1})

    def tearDown(self):
        _clean()

    def test_low_stock_report_flags_item(self):
        report = rp.low_stock_report()
        self.assertIn("BR001", report)

    def test_revenue_summary_totals(self):
        report = rp.revenue_summary()
        # (2*40) + (1*300 + 1*40) = 80 + 340 = 420
        self.assertIn("420.00", report)

    def test_best_sellers_ranks_bread_first(self):
        report = rp.best_sellers_report()
        # Bread sold 3 units total vs Cake's 1 unit -> bread should rank first
        lines = report.splitlines()
        bread_line_idx = next(i for i, l in enumerate(lines) if "BR001" in l)
        cake_line_idx = next(i for i, l in enumerate(lines) if "CAKE01" in l)
        self.assertLess(bread_line_idx, cake_line_idx)


if __name__ == "__main__":
    unittest.main()
