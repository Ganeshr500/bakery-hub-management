"""
make_diagrams.py
-----------------
Generates all design diagrams (architecture, workflow, use case, class,
sequence, schema) as PNG images for the project report, using matplotlib
so no external tools or network access are required.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Ellipse
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

NAVY = "#1f3a5f"
BLUE = "#3b6ea5"
LIGHT = "#eaf1fa"
GREY = "#555555"


def new_fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc=LIGHT, ec=NAVY, fontsize=10, fontweight="normal"):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.08",
                        linewidth=1.6, edgecolor=ec, facecolor=fc, zorder=2)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fontsize, color="#111111", fontweight=fontweight, zorder=3, wrap=True)
    return b


def arrow(ax, x1, y1, x2, y2, text=None, style="-|>", color=GREY, connectionstyle="arc3,rad=0.0"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14,
                         color=color, linewidth=1.4, connectionstyle=connectionstyle, zorder=1)
    ax.add_patch(a)
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.15, text, ha="center", fontsize=8, color=color)


# ---------------------------------------------------------------------
# 1. SYSTEM ARCHITECTURE DIAGRAM
# ---------------------------------------------------------------------
def architecture_diagram():
    fig, ax = new_fig(11, 7)
    ax.text(5.5, 6.6, "BakeryHub - System Architecture", ha="center", fontsize=15, fontweight="bold", color=NAVY)

    box(ax, 3.7, 5.3, 3.6, 0.9, "User (CLI Console)", fc="#fff3d6", fontweight="bold")
    box(ax, 3.7, 3.9, 3.6, 0.9, "Presentation Layer\nmain.py (menu-driven CLI)", fontweight="bold")

    box(ax, 0.3, 2.4, 3.1, 1.0, "Module 1\ninventory_manager.py\n(CRUD)")
    box(ax, 3.95, 2.4, 3.1, 1.0, "Module 2\norder_processing.py\n(Orders + Stock)")
    box(ax, 7.6, 2.4, 3.1, 1.0, "Module 3\nreports.py\n(Analytics)")

    box(ax, 1.6, 1.1, 3.0, 0.8, "models.py\n(BakeryItem, Order)")
    box(ax, 4.75, 1.1, 3.0, 0.8, "utils.py / exceptions.py\n(validation, errors, logging)")

    box(ax, 3.4, 0.05, 4.2, 0.75, "storage.py -> items.json / orders.json", fc="#e3f6e3")

    arrow(ax, 5.5, 5.3, 5.5, 4.8)
    for cx in (1.85, 5.5, 9.15):
        arrow(ax, 5.5, 3.9, cx, 3.4)
    arrow(ax, 1.85, 2.4, 3.1, 1.9)
    arrow(ax, 5.5, 2.4, 5.5, 1.9)
    arrow(ax, 9.15, 2.4, 6.4, 1.9)
    arrow(ax, 5.5, 1.1, 5.5, 0.8)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "01_architecture.png"), dpi=170)
    plt.close(fig)


# ---------------------------------------------------------------------
# 2. WORKFLOW / PROCESS FLOW DIAGRAM
# ---------------------------------------------------------------------
def workflow_diagram():
    W = 13.6
    fig, ax = new_fig(W, 7.0)
    ax.text(W / 2, 6.55, "Process Flow - Placing a Customer Order", ha="center",
            fontsize=15, fontweight="bold", color=NAVY)

    steps = [
        "Start\nApplication",
        "Display\nMain Menu",
        "Choose 'Place\nOrder'",
        "Enter items\n& quantities",
        "Check stock\navailability",
        "Deduct stock,\ncompute total",
        "Save order &\nshow receipt",
    ]
    n = len(steps)
    w = 1.55
    gap = 0.28
    total = n * w + (n - 1) * gap
    x = (W - total) / 2
    y = 3.6

    box_xs = []
    for i, s in enumerate(steps):
        fc = "#fff3d6" if i == 0 else ("#e3f6e3" if i == n - 1 else LIGHT)
        box(ax, x, y, w, 1.7, s, fc=fc, fontsize=8.3)
        box_xs.append(x)
        if i < n - 1:
            arrow(ax, x + w, y + 0.85, x + w + gap, y + 0.85)
        x += w + gap

    last_x = box_xs[-1] + w / 2
    second_x = box_xs[1] + w / 2
    arrow(ax, last_x, y - 0.05, second_x, y - 0.05, text="loop until user chooses Exit",
          connectionstyle="arc3,rad=0.5", color=NAVY)

    stock_x = box_xs[4] + w / 2
    ax.annotate("Insufficient stock ->\nreject order, show error",
                xy=(stock_x, y - 0.05), xytext=(stock_x, y - 1.7),
                ha="center", fontsize=8, color="#a33",
                arrowprops=dict(arrowstyle="-|>", color="#a33"))

    ax.set_ylim(0.2, 7.0)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "02_workflow.png"), dpi=170)
    plt.close(fig)


# ---------------------------------------------------------------------
# 3. USE CASE DIAGRAM
# ---------------------------------------------------------------------
def use_case_diagram():
    fig, ax = new_fig(9, 7)
    ax.text(4.5, 6.6, "Use Case Diagram - BakeryHub", ha="center", fontsize=15, fontweight="bold", color=NAVY)

    ax_x, ax_y = 0.9, 3.4
    ax.plot([ax_x], [ax_y + 0.9], marker="o", markersize=18, color=NAVY)
    ax.plot([ax_x, ax_x], [ax_y + 0.55, ax_y - 0.1], color=NAVY, linewidth=2)
    ax.plot([ax_x - 0.35, ax_x + 0.35], [ax_y + 0.35, ax_y + 0.35], color=NAVY, linewidth=2)
    ax.plot([ax_x, ax_x - 0.3], [ax_y - 0.1, ax_y - 0.6], color=NAVY, linewidth=2)
    ax.plot([ax_x, ax_x + 0.3], [ax_y - 0.1, ax_y - 0.6], color=NAVY, linewidth=2)
    ax.text(ax_x, ax_y - 1.0, "Bakery\nStaff / Owner\n(User)", ha="center", fontsize=9, fontweight="bold")

    ax.add_patch(Rectangle((2.6, 0.6), 6.0, 5.6, fill=False, linewidth=1.6, edgecolor=NAVY))
    ax.text(5.6, 6.05, "BakeryHub System", ha="center", fontsize=10, fontweight="bold", color=NAVY)

    use_cases = [
        "Add / Update /\nDelete Item", "Restock Item",
        "Place Order", "Cancel Order",
        "View Low Stock\nReport", "View Revenue &\nBest-Sellers",
    ]
    positions = [(3.1, 4.9), (3.1, 3.75), (3.1, 2.55), (5.6, 4.9), (5.6, 3.75), (5.6, 2.55)]
    for (ux, uy), text in zip(positions, use_cases):
        e = Ellipse((ux + 1.05, uy + 0.35), 2.5, 0.95, facecolor=LIGHT, edgecolor=BLUE, linewidth=1.4, zorder=2)
        ax.add_patch(e)
        ax.text(ux + 1.05, uy + 0.35, text, ha="center", va="center", fontsize=8.3, zorder=3)
        arrow(ax, ax_x + 0.3, ax_y + 0.3, ux, uy + 0.35, color=GREY)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "03_use_case.png"), dpi=170)
    plt.close(fig)


# ---------------------------------------------------------------------
# 4. CLASS DIAGRAM
# ---------------------------------------------------------------------
def class_diagram():
    fig, ax = new_fig(11, 6.5)
    ax.text(5.5, 6.1, "Class Diagram - Core Classes", ha="center", fontsize=15, fontweight="bold", color=NAVY)

    def class_box(x, y, w, h, title, attrs, methods):
        box(ax, x, y, w, h, "", fc=LIGHT)
        ax.plot([x, x + w], [y + h - 0.55, y + h - 0.55], color=NAVY, linewidth=1.2)
        mid_y = y + h - 0.55 - (0.32 * len(attrs)) - 0.15
        ax.plot([x, x + w], [mid_y, mid_y], color=NAVY, linewidth=1.2)
        ax.text(x + w / 2, y + h - 0.3, title, ha="center", fontsize=10, fontweight="bold")
        for i, a in enumerate(attrs):
            ax.text(x + 0.15, y + h - 0.75 - i * 0.32, a, fontsize=8, va="top")
        for i, m in enumerate(methods):
            ax.text(x + 0.15, mid_y - 0.2 - i * 0.32, m, fontsize=8, va="top")

    class_box(0.2, 1.0, 3.5, 5.0, "BakeryItem",
              ["- item_id: str", "- name: str", "- category: str",
               "- unit_price: float", "- stock_qty: int", "- reorder_level: int"],
              ["+ to_dict()", "+ from_dict(data)", "+ is_low_stock()"])

    class_box(4.0, 1.0, 3.3, 5.0, "Order",
              ["- order_id: str", "- customer_name: str", "- line_items: dict",
               "- total_amount: float", "- timestamp: str", "- status: str"],
              ["+ to_dict()", "+ from_dict(data)"])

    class_box(7.6, 1.0, 3.1, 5.0, "reports\n(module functions)",
              [" "],
              ["+ low_stock_report()", "+ revenue_summary()", "+ best_sellers_report()"])

    arrow(ax, 3.7, 3.5, 4.0, 3.5, text="referenced by")
    arrow(ax, 7.3, 3.5, 7.6, 3.5, text="reads")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "04_class_diagram.png"), dpi=170)
    plt.close(fig)


# ---------------------------------------------------------------------
# 5. SEQUENCE DIAGRAM (Place Order flow)
# ---------------------------------------------------------------------
def sequence_diagram():
    fig, ax = new_fig(11, 7)
    ax.text(5.5, 6.6, "Sequence Diagram - Place Order", ha="center",
            fontsize=14, fontweight="bold", color=NAVY)

    actors = ["User", "main.py", "order_processing.py", "storage.py", "inventory_manager.py"]
    xs = [0.9, 2.8, 5.3, 7.8, 10.0]
    for x, a in zip(xs, actors):
        box(ax, x - 0.8, 5.6, 1.6, 0.7, a, fontsize=8, fontweight="bold")
        ax.plot([x, x], [0.4, 5.6], color="#aaaaaa", linestyle="--", linewidth=1)

    msgs = [
        (0, 1, 5.15, "place order (customer, cart)"),
        (1, 2, 4.7, "place_order()"),
        (2, 3, 4.25, "load_items()"),
        (3, 2, 3.85, "return item stock data"),
        (2, 2, 3.45, "validate stock for\nevery cart line"),
        (2, 3, 3.05, "save_items()\n(deduct stock)"),
        (2, 3, 2.65, "save_orders()\n(new order record)"),
        (2, 1, 2.25, "return Order object"),
        (1, 0, 1.85, "show order total\n& confirmation"),
    ]
    for src, dst, y, text in msgs:
        arrow(ax, xs[src], y, xs[dst], y, text=text)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "05_sequence.png"), dpi=170)
    plt.close(fig)


# ---------------------------------------------------------------------
# 6. SCHEMA / DATA MODEL DIAGRAM
# ---------------------------------------------------------------------
def schema_diagram():
    fig, ax = new_fig(9, 6.5)
    ax.text(4.5, 6.1, "Storage Schema - items.json & orders.json", ha="center",
            fontsize=14, fontweight="bold", color=NAVY)

    box(ax, 0.6, 3.9, 3.7, 1.7,
        '"BR001": {\n'
        '  "name": "White Bread",\n'
        '  "category": "Bread",\n'
        '  "unit_price": 40,\n'
        '  "stock_qty": 48,\n'
        '  "reorder_level": 10\n'
        '}', fc="#fff3d6", fontsize=8)

    box(ax, 4.8, 3.9, 3.6, 1.7,
        '"ORD0001": {\n'
        '  "customer_name": "Asha",\n'
        '  "line_items": {"BR001": 2},\n'
        '  "total_amount": 80.0,\n'
        '  "status": "COMPLETED"\n'
        '}', fc="#e3f6e3", fontsize=8)

    ax.text(4.5, 3.3, "items.json (keyed by item_id)              orders.json (keyed by order_id)",
            ha="center", fontsize=8, color=GREY)

    arrow(ax, 3.6, 3.9, 4.9, 3.9, text="order references item_id", color=NAVY)

    ax.text(4.5, 1.2,
            "Two separate JSON files: items.json holds product/stock data;\n"
            "orders.json holds each transaction, linking back to item_id(s)\n"
            "and recording the quantity purchased and total amount.",
            ha="center", fontsize=8.5, color=GREY)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "06_schema.png"), dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    architecture_diagram()
    workflow_diagram()
    use_case_diagram()
    class_diagram()
    sequence_diagram()
    schema_diagram()
    print("All diagrams generated.")
