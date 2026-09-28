"""
main.py
-------
Entry point for BakeryHub. Presents a menu-driven CLI that ties together
all three functional modules:
    1) Inventory Management (CRUD)
    2) Order Processing
    3) Reports & Analytics
"""

import inventory_manager as im
import order_processing as op
import reports as rp
from config import CATEGORIES
from exceptions import BakeryHubError
from utils import get_logger

logger = get_logger("main")

MENU = """
=========================================
        BAKERYHUB - MAIN MENU
=========================================
 1. Add new item
 2. View all items
 3. View one item's details
 4. Update item price
 5. Restock item
 6. Delete item
 7. Place new order
 8. View order details
 9. Cancel an order
10. Low stock report
11. Revenue summary
12. Best-sellers report
 0. Exit
=========================================
"""


def prompt(text: str) -> str:
    return input(text).strip()


def handle_add_item():
    item_id = prompt("Item ID (e.g. BR001): ")
    name = prompt("Item name: ")
    print(f"Categories: {', '.join(CATEGORIES)}")
    category = prompt("Category: ")
    price = prompt("Unit price: ")
    qty = prompt("Initial stock quantity: ")
    item = im.add_item(item_id, name, category, price, qty)
    print(f"✔ Added: {item}")


def handle_list_items():
    items = im.list_items()
    if not items:
        print("No items in inventory yet.")
        return
    print(f"\n{'ID':<8}{'Name':<20}{'Category':<10}{'Price':<10}{'Stock':<8}")
    print("-" * 56)
    for i in items:
        flag = " (LOW)" if i.is_low_stock() else ""
        print(f"{i.item_id:<8}{i.name:<20}{i.category:<10}{i.unit_price:<10}{str(i.stock_qty)+flag:<8}")


def handle_view_item():
    item_id = prompt("Item ID: ")
    item = im.get_item(item_id)
    print(f"\nID: {item.item_id} | {item.name} | {item.category}")
    print(f"Price: {item.unit_price} | Stock: {item.stock_qty} | Reorder level: {item.reorder_level}")


def handle_update_price():
    item_id = prompt("Item ID: ")
    price = prompt("New price: ")
    item = im.update_item_price(item_id, price)
    print(f"✔ Updated: {item}")


def handle_restock():
    item_id = prompt("Item ID: ")
    qty = prompt("Additional quantity: ")
    item = im.restock_item(item_id, qty)
    print(f"✔ Restocked: {item}")


def handle_delete_item():
    item_id = prompt("Item ID: ")
    im.delete_item(item_id)
    print(f"✔ Deleted item {item_id}")


def handle_place_order():
    customer_name = prompt("Customer name: ")
    cart = {}
    print("Enter items for this order. Leave Item ID blank to finish.")
    while True:
        item_id = prompt("  Item ID: ")
        if not item_id:
            break
        qty = prompt("  Quantity: ")
        cart[item_id] = qty
    order = op.place_order(customer_name, cart)
    print(f"✔ Order placed: {order.order_id} | Total: {order.total_amount}")


def handle_view_order():
    order_id = prompt("Order ID: ")
    order = op.get_order(order_id)
    print(f"\nOrder {order.order_id} | {order.customer_name} | {order.status}")
    print(f"Items: {order.line_items}")
    print(f"Total: {order.total_amount} | Placed: {order.timestamp}")


def handle_cancel_order():
    order_id = prompt("Order ID to cancel: ")
    order = op.cancel_order(order_id)
    print(f"✔ Order {order.order_id} cancelled, stock restored.")


def handle_low_stock():
    print(rp.low_stock_report())


def handle_revenue():
    print(rp.revenue_summary())


def handle_best_sellers():
    print(rp.best_sellers_report())


ACTIONS = {
    "1": handle_add_item,
    "2": handle_list_items,
    "3": handle_view_item,
    "4": handle_update_price,
    "5": handle_restock,
    "6": handle_delete_item,
    "7": handle_place_order,
    "8": handle_view_order,
    "9": handle_cancel_order,
    "10": handle_low_stock,
    "11": handle_revenue,
    "12": handle_best_sellers,
}


def main():
    logger.info("BakeryHub application started")
    print("Welcome to BakeryHub!")
    while True:
        print(MENU)
        choice = prompt("Enter choice: ")
        if choice == "0":
            print("Goodbye!")
            logger.info("BakeryHub application exited normally")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice, please try again.")
            continue
        try:
            action()
        except BakeryHubError as e:
            # Expected, user-facing errors: show a clean message, keep running
            print(f"⚠ Error: {e}")
            logger.warning(f"Handled error: {e}")
        except Exception as e:
            # Unexpected errors: log full detail, don't crash the app
            print("⚠ An unexpected error occurred. Check logs/app.log for details.")
            logger.exception(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
