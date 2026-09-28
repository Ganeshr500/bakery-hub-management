"""
reports.py
----------
FUNCTIONAL MODULE 3: Reports & Analytics
Generates inventory and sales reports: low-stock alerts, revenue summary,
and best-selling item analysis.
"""

from collections import defaultdict
from inventory_manager import list_items
from order_processing import list_orders
from utils import get_logger

logger = get_logger(__name__)


def low_stock_report() -> str:
    """List every item at or below its reorder level."""
    items = list_items()
    low = [i for i in items if i.is_low_stock()]

    lines = ["=" * 46, " LOW STOCK ALERT REPORT", "=" * 46]
    if not low:
        lines.append("  All items are adequately stocked.")
    else:
        lines.append(f"  {'Item ID':<10}{'Name':<20}{'Stock':<8}{'Reorder Lvl':<12}")
        lines.append("-" * 46)
        for i in low:
            lines.append(f"  {i.item_id:<10}{i.name:<20}{i.stock_qty:<8}{i.reorder_level:<12}")
    lines.append("=" * 46)

    logger.info(f"Generated low-stock report ({len(low)} item(s) flagged)")
    return "\n".join(lines)


def revenue_summary() -> str:
    """Summarize total revenue, order count, and average order value."""
    orders = [o for o in list_orders() if o.status == "COMPLETED"]

    lines = ["=" * 46, " REVENUE SUMMARY", "=" * 46]
    if not orders:
        lines.append("  No completed orders yet.")
        lines.append("=" * 46)
        return "\n".join(lines)

    total_revenue = sum(o.total_amount for o in orders)
    avg_order_value = round(total_revenue / len(orders), 2)

    lines.append(f"  Completed orders     : {len(orders)}")
    lines.append(f"  Total revenue        : {total_revenue:.2f}")
    lines.append(f"  Average order value  : {avg_order_value:.2f}")
    lines.append("=" * 46)

    logger.info("Generated revenue summary report")
    return "\n".join(lines)


def best_sellers_report(top_n: int = 5) -> str:
    """Rank items by total quantity sold across all completed orders."""
    orders = [o for o in list_orders() if o.status == "COMPLETED"]
    items_by_id = {i.item_id: i for i in list_items()}

    qty_sold = defaultdict(int)
    for order in orders:
        for item_id, qty in order.line_items.items():
            qty_sold[item_id] += qty

    lines = ["=" * 46, f" TOP {top_n} BEST-SELLING ITEMS", "=" * 46]
    if not qty_sold:
        lines.append("  No sales recorded yet.")
    else:
        ranked = sorted(qty_sold.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
        lines.append(f"  {'Rank':<6}{'Item ID':<10}{'Name':<20}{'Units Sold':<10}")
        lines.append("-" * 46)
        for rank, (item_id, qty) in enumerate(ranked, start=1):
            name = items_by_id[item_id].name if item_id in items_by_id else "(deleted item)"
            lines.append(f"  {rank:<6}{item_id:<10}{name:<20}{qty:<10}")
    lines.append("=" * 46)

    logger.info("Generated best-sellers report")
    return "\n".join(lines)
