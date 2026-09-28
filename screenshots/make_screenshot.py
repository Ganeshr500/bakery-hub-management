import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
config.ITEMS_FILE = os.path.join(config.DATA_DIR, "items_demo.json")
config.ITEMS_BACKUP_FILE = os.path.join(config.DATA_DIR, "items_demo_backup.json")
config.ORDERS_FILE = os.path.join(config.DATA_DIR, "orders_demo.json")
config.ORDERS_BACKUP_FILE = os.path.join(config.DATA_DIR, "orders_demo_backup.json")

import inventory_manager as im
import order_processing as op
import reports as rp

for f in (config.ITEMS_FILE, config.ITEMS_BACKUP_FILE, config.ORDERS_FILE, config.ORDERS_BACKUP_FILE):
    if os.path.exists(f):
        os.remove(f)

im.add_item("BR001", "White Bread", "Bread", 40, 8, reorder_level=10)
im.add_item("CAKE01", "Chocolate Cake", "Cake", 300, 20)
im.add_item("COOK01", "Butter Cookie", "Cookie", 15, 100)

op.place_order("Asha Patel", {"BR001": 2, "COOK01": 10})
op.place_order("Rahul Verma", {"CAKE01": 1, "BR001": 1})

output_text = rp.low_stock_report() + "\n\n" + rp.revenue_summary() + "\n\n" + rp.best_sellers_report()

fig, ax = plt.subplots(figsize=(7.5, 7.2))
ax.axis("off")
fig.patch.set_facecolor("#1e1e1e")
ax.set_facecolor("#1e1e1e")
ax.text(0.02, 0.98, "$ python3 main.py   (sample output)", color="#8fd18f",
        fontsize=10, family="monospace", va="top", transform=ax.transAxes)
ax.text(0.02, 0.92, output_text, color="#e6e6e6", fontsize=8.0,
        family="monospace", va="top", transform=ax.transAxes)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_output.png"),
            dpi=170, facecolor=fig.get_facecolor())

for f in (config.ITEMS_FILE, config.ITEMS_BACKUP_FILE, config.ORDERS_FILE, config.ORDERS_BACKUP_FILE):
    if os.path.exists(f):
        os.remove(f)

print("Screenshot generated.")
