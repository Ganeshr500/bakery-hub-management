"""
build_report.py
----------------
Builds the full project report PDF (report/BakeryHub_Project_Report.pdf)
covering all 15 sections required by the VITyarthi submission guidelines.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, ListFlowable,
    ListItem, Table, TableStyle
)

BASE = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS = os.path.join(BASE, "diagrams")
SCREENSHOTS = os.path.join(BASE, "screenshots")
OUT_DIR = os.path.join(BASE, "report")
os.makedirs(OUT_DIR, exist_ok=True)
OUT_FILE = os.path.join(OUT_DIR, "BakeryHub_Project_Report.pdf")

NAVY = colors.HexColor("#1f3a5f")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], textColor=NAVY, spaceBefore=14, spaceAfter=8))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], textColor=NAVY, spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="BodyText2", parent=styles["BodyText"], fontSize=10.3, leading=15, spaceAfter=6))
styles.add(ParagraphStyle(name="Caption", parent=styles["BodyText"], fontSize=8.5, textColor=colors.grey,
                           alignment=TA_CENTER, spaceAfter=14))
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontSize=26, textColor=NAVY, spaceAfter=6))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontSize=13, alignment=TA_CENTER,
                           textColor=colors.HexColor("#444444"), spaceAfter=4))
styles.add(ParagraphStyle(name="Mono", parent=styles["Normal"], fontName="Courier", fontSize=8.3, leading=11,
                           backColor=colors.HexColor("#f5f5f5")))

story = []


def h1(text):
    story.append(Paragraph(text, styles["H1"]))


def h2(text):
    story.append(Paragraph(text, styles["H2"]))


def p(text):
    story.append(Paragraph(text, styles["BodyText2"]))


def bullets(items):
    story.append(ListFlowable(
        [ListItem(Paragraph(i, styles["BodyText2"])) for i in items],
        bulletType="bullet", start="•", leftIndent=16,
    ))
    story.append(Spacer(1, 6))


def diagram(filename, caption, width=15.5 * cm):
    path = os.path.join(DIAGRAMS, filename)
    img = Image(path, width=width, height=width * 0.62)
    story.append(img)
    story.append(Paragraph(caption, styles["Caption"]))


def code_block(text):
    story.append(Paragraph(text.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles["Mono"]))
    story.append(Spacer(1, 8))


# =====================================================================
# 1. COVER PAGE
# =====================================================================
story.append(Spacer(1, 5 * cm))
story.append(Paragraph("BakeryHub", styles["CoverTitle"]))
story.append(Paragraph("Bakery Inventory, Orders &amp; Sales Analytics System", styles["CoverSub"]))
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("Project Report", styles["CoverSub"]))
story.append(Spacer(1, 2 * cm))
story.append(Paragraph("Submitted for: Python Programming (First Semester)", styles["CoverSub"]))
story.append(Paragraph("Submission Type: VITyarthi - Build Your Own Project", styles["CoverSub"]))
story.append(Paragraph("Language / Stack: Python 3 (Standard Library)", styles["CoverSub"]))
story.append(PageBreak())

# =====================================================================
# 2. INTRODUCTION
# =====================================================================
h1("1. Introduction")
p("Small bakeries often track stock and sales using handwritten registers "
  "or basic spreadsheets. This makes it easy to lose track of remaining "
  "stock, to accidentally sell more than is actually available, and to "
  "answer simple business questions like &quot;what's our best-selling item?&quot; "
  "or &quot;which items are about to run out?&quot; quickly and reliably.")
p("<b>BakeryHub</b> is a console-based Python application built to apply the "
  "core concepts covered in a first-semester Python course &mdash; variables, control "
  "flow, functions, data structures (lists/dictionaries), file handling, exception "
  "handling, basic object-oriented programming, and the standard <b>logging</b> and "
  "<b>unittest</b> modules &mdash; to a real, practical small-business problem. It is "
  "organised into three functional modules and a small set of supporting utility "
  "modules, all coordinated by a single menu-driven command-line interface.")

# =====================================================================
# 3. PROBLEM STATEMENT
# =====================================================================
h1("2. Problem Statement")
p("A bakery needs a lightweight, dependable way to record what products it "
  "sells, how much stock of each is left, and to process customer orders "
  "such that stock is checked and deducted correctly, bills are computed "
  "accurately, and simple sales reports can be generated on demand &mdash; without "
  "relying on manual spreadsheet formulas or paper registers that are easy "
  "to lose or miscalculate.")
p("The project's goal is to design and build a small but complete system that "
  "solves this end-to-end: from adding items to inventory, through placing and "
  "cancelling orders with correct stock handling, to generating low-stock alerts "
  "and revenue analytics &mdash; while remaining simple enough to be fully understood, "
  "tested, and extended by a first-semester Python student.")

# =====================================================================
# 4. FUNCTIONAL REQUIREMENTS
# =====================================================================
h1("3. Functional Requirements")
p("The system implements <b>three major functional modules</b>, each with a clear "
  "input/output contract and a logical place in the overall workflow:")
h2("3.1 Module 1 &mdash; Inventory Management (CRUD)")
bullets([
    "Add a new bakery item (ID, name, category, price, stock), rejecting duplicates.",
    "View a single item's full record, or list all items with a low-stock flag.",
    "Update an item's unit price, or restock it after a fresh baking batch.",
    "Delete an item record permanently.",
])
h2("3.2 Module 2 &mdash; Order Processing")
bullets([
    "Place a multi-item order for a customer: every line is validated for "
    "sufficient stock <i>before</i> anything is deducted.",
    "On success, stock is deducted, the bill total is computed, and the "
    "order is saved with a generated order ID.",
    "Cancel an existing order, automatically restoring the stock it had consumed.",
])
h2("3.3 Module 3 &mdash; Reports &amp; Analytics")
bullets([
    "Low-stock alert report: lists every item at or below its reorder level.",
    "Revenue summary: total completed orders, total revenue, average order value.",
    "Best-sellers report: ranks items by total quantity sold across all orders.",
])
p("<b>Input/Output structure:</b> all inputs are simple typed values collected via "
  "console prompts (item ID, name, category, price, quantity, customer name); all "
  "outputs are either confirmation messages, tabular listings, or formatted "
  "multi-line report text printed to the console.")
p("<b>Workflow:</b> the user always starts at the main menu, selects a numbered "
  "option, is guided through any required prompts, sees the result of the "
  "operation immediately, and is returned to the main menu &mdash; see the Process "
  "Flow diagram in Section 6.")

# =====================================================================
# 5. NON-FUNCTIONAL REQUIREMENTS
# =====================================================================
h1("4. Non-Functional Requirements")
nfr_data = [
    ["Requirement", "How BakeryHub addresses it"],
    ["Performance", "In-memory dict lookups (O(1) by item_id/order_id) after a "
                     "single database read per operation; no unnecessary re-reads."],
    ["Reliability", "All inventory and order data lives in a SQLite database "
                     "(data/bakeryhub.db). Orders validate all cart lines before "
                     "deducting any stock, so a rejected order never leaves "
                     "inventory half-updated."],
    ["Usability", "Clear numbered menu, consistent prompts, aligned tabular output, "
                   "and human-readable reports."],
    ["Maintainability", "Code is split into 9 single-purpose modules with docstrings; "
                         "constants live in one config.py file."],
    ["Error handling", "A custom exception hierarchy (exceptions.py) distinguishes "
                        "expected user errors (e.g. insufficient stock) from "
                        "unexpected bugs; all are caught in main.py."],
    ["Logging / Monitoring", "Every add/update/delete/order/cancel and every warning "
                              "or unexpected error is timestamped and written to logs/app.log."],
    ["Security", "All user input is validated with regular expressions/range checks "
                 "before being stored (item ID format, price range, quantity range)."],
    ["Scalability", "The storage layer (storage.py) is isolated behind simple "
                     "load/save functions, backed by a SQLite database "
                     "(database.py), so a larger client-server database could "
                     "be swapped in later without touching business logic."],
]
t = Table(nfr_data, colWidths=[4.2 * cm, 11.3 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef3f9")]),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 10))
story.append(PageBreak())

# =====================================================================
# 6. SYSTEM ARCHITECTURE
# =====================================================================
h1("5. System Architecture")
p("BakeryHub follows a simple layered architecture: a presentation layer "
  "(the CLI in main.py), three functional modules that contain the business "
  "logic, shared support modules (models, utils, exceptions), and a storage "
  "layer (storage.py + database.py) that isolates all database I/O to a "
  "single SQLite database file.")
diagram("01_architecture.png", "Figure 1: System Architecture Diagram")

# =====================================================================
# 7. DESIGN DIAGRAMS
# =====================================================================
h1("6. Design Diagrams")
h2("6.1 Process Flow / Workflow Diagram")
p("Describes the flow of placing a customer order, including the "
  "stock-validation branch and the loop back to the main menu.")
diagram("02_workflow.png", "Figure 2: Process Flow Diagram")
story.append(PageBreak())

h2("6.2 Use Case Diagram")
p("Shows the single actor (Bakery Staff/Owner) and the six primary use "
  "cases exposed by the system.")
diagram("03_use_case.png", "Figure 3: Use Case Diagram")
story.append(PageBreak())

h2("6.3 Class Diagram")
p("BakeryItem and Order are the two data classes in the system "
  "(first-semester OOP scope); the reports module uses plain functions "
  "grouped by responsibility, shown here as a module box for clarity.")
diagram("04_class_diagram.png", "Figure 4: Class Diagram")
story.append(PageBreak())

h2("6.4 Sequence Diagram")
p("Illustrates the interaction between the CLI, the order-processing "
  "module, the storage layer, and inventory data for a typical "
  "&quot;place an order&quot; user action.")
diagram("05_sequence.png", "Figure 5: Sequence Diagram")
story.append(PageBreak())

h2("6.5 Storage Schema (Database/Storage Design)")
p("BakeryHub persists data in a local SQLite database (data/bakeryhub.db). "
  "The diagram below documents the schema: an items table keyed by item "
  "ID, and an orders table keyed by order ID, with each order's line items "
  "stored as a JSON-encoded field referencing the item IDs it purchased.")
diagram("06_schema.png", "Figure 6: Storage Schema Diagram")

# =====================================================================
# 8. DESIGN DECISIONS & RATIONALE
# =====================================================================
h1("7. Design Decisions &amp; Rationale")
bullets([
    "<b>SQLite over a client-server database:</b> chosen because it needs no "
    "separate server process or setup, ships with Python's standard library "
    "(sqlite3), and still gives real relational storage with a clear "
    "migration path to a larger database engine later if the bakery grows.",
    "<b>Two tables (items / orders):</b> keeps product catalogue data and "
    "transaction history independently queryable, mirroring how separate "
    "tables would work in any relational database.",
    "<b>Validate-then-deduct ordering logic:</b> every line in a cart is "
    "checked against available stock <i>before</i> any stock is deducted, so a "
    "multi-item order can never partially succeed and leave inventory "
    "inconsistent.",
    "<b>Custom exception hierarchy:</b> lets main.py distinguish expected, "
    "user-facing problems (e.g. insufficient stock) from genuine bugs, "
    "so the application never crashes on bad input.",
    "<b>Whole-table replace on save:</b> save_items()/save_orders() rewrite "
    "the relevant table inside a single transaction, so an interrupted save "
    "can't leave the database half-updated.",
    "<b>Menu-driven CLI over argument-based CLI:</b> more approachable for the "
    "target user (bakery staff, not necessarily technical) than remembering "
    "command-line flags.",
])

# =====================================================================
# 9. IMPLEMENTATION DETAILS
# =====================================================================
h1("8. Implementation Details")
p("The project consists of <b>10 Python modules</b> plus a test module, organised as follows:")
impl_data = [
    ["File", "Responsibility"],
    ["config.py", "Constants: file/database paths, categories, reorder level, price/qty limits."],
    ["exceptions.py", "Custom exception classes (ItemNotFoundError, InsufficientStockError, etc.)."],
    ["models.py", "BakeryItem and Order classes: data models + to_dict/from_dict."],
    ["database.py", "SQLite connection handling and schema creation (items, orders tables)."],
    ["storage.py", "Load/save for items and orders against the SQLite database."],
    ["utils.py", "Logger factory + regex/range-based input validation helpers."],
    ["inventory_manager.py", "Module 1: add/get/list/update/restock/delete item (CRUD)."],
    ["order_processing.py", "Module 2: place_order, cancel_order, stock validation/deduction."],
    ["reports.py", "Module 3: low-stock, revenue, and best-sellers reports."],
    ["main.py", "Presentation layer: menu loop, prompts, top-level error handling."],
    ["tests/test_bakeryhub.py", "16 unit tests covering all three functional modules."],
]
t2 = Table(impl_data, colWidths=[4.8 * cm, 10.7 * cm])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Courier"),
    ("FONTSIZE", (0, 0), (-1, -1), 8.7),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef3f9")]),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t2)
story.append(Spacer(1, 10))
p("Sample core logic &mdash; validating stock before deducting anything (order_processing.py):")
code_block(
    'for item_id, qty in cart.items():\n'
    '    if qty > items[item_id]["stock_qty"]:\n'
    '        raise InsufficientStockError(item_id, qty, items[item_id]["stock_qty"])\n'
    '    clean_cart[item_id] = qty\n'
    '# only after EVERY line passes validation do we deduct stock'
)

# =====================================================================
# 10. SCREENSHOTS / RESULTS
# =====================================================================
story.append(PageBreak())
h1("9. Screenshots / Results")
p("Sample console output from a real run of the application, showing the "
  "low-stock alert report, revenue summary, and best-sellers report:")
diagram("../screenshots/sample_output.png", "Figure 7: Sample console output (reports)",
        width=13 * cm)

# =====================================================================
# 11. TESTING APPROACH
# =====================================================================
h1("10. Testing Approach")
p("Automated unit tests are written using Python's built-in <b>unittest</b> "
  "framework in <font face='Courier'>tests/test_bakeryhub.py</font>. Tests "
  "run against a separate temporary SQLite database so real data is never "
  "touched, and setUp/tearDown ensure each test starts from a clean state.")
bullets([
    "<b>Inventory Manager:</b> add + retrieve, duplicate rejection, missing-item "
    "lookup, invalid category rejection, restock + price update, low-stock flag, delete.",
    "<b>Order Processing:</b> stock deduction &amp; total calculation, insufficient-stock "
    "rejection with no partial deduction, unknown item rejection, cancel restores "
    "stock, cancelling a missing order raises an error, empty cart rejected.",
    "<b>Reports:</b> low-stock report flags the right item, revenue summary totals "
    "are correct, best-sellers ranks the higher-selling item first.",
])
p("Result: <b>16 / 16 tests pass</b> (verified via "
  "<font face='Courier'>python -m unittest tests/test_bakeryhub.py -v</font>). "
  "Manual end-to-end testing was also performed by piping a full menu-driven "
  "session (add items, place an order, view reports) into "
  "<font face='Courier'>main.py</font> and confirming correct output.")

# =====================================================================
# 12. CHALLENGES FACED
# =====================================================================
h1("11. Challenges Faced")
bullets([
    "<b>Avoiding partial stock deduction:</b> if one item in a multi-item order "
    "had insufficient stock, earlier lines could already have been deducted; "
    "solved by validating <i>every</i> line in the cart first, and only deducting "
    "stock once the whole order is confirmed valid.",
    "<b>Generating unique, readable order IDs:</b> solved with a small helper "
    "that scans existing order IDs and increments the highest number found "
    "(e.g. ORD0001 -> ORD0002).",
    "<b>Keeping cancellation consistent:</b> cancelling an order needed to "
    "restore exactly the stock that was deducted, and to prevent cancelling "
    "an already-cancelled order; solved by checking order status before "
    "restoring stock.",
])

# =====================================================================
# 13. LEARNINGS & KEY TAKEAWAYS
# =====================================================================
h1("12. Learnings &amp; Key Takeaways")
bullets([
    "Validating an entire batch of input <i>before</i> making any changes is a "
    "simple but powerful pattern for keeping data consistent.",
    "Splitting a program into small, single-purpose modules (even in a CLI "
    "project) makes it far easier to test and reason about than one large script.",
    "Writing unit tests alongside the modules (not after) caught several bugs "
    "early, e.g. the empty-cart edge case and duplicate item-ID handling.",
    "A thin, isolated storage layer (storage.py + database.py) meant moving "
    "persistence from flat JSON files to a real SQLite database required no "
    "changes at all to the inventory, order, or reporting logic above it.",
])

# =====================================================================
# 14. FUTURE ENHANCEMENTS
# =====================================================================
h1("13. Future Enhancements")
bullets([
    "Migrate from SQLite to a client-server database (PostgreSQL/MySQL) for "
    "true multi-user, concurrent access across several tills at once.",
    "Add a simple GUI (Tkinter) or web front-end (Flask) over the same modules.",
    "Support multiple branches/locations with separate inventories.",
    "Add expiry-date tracking for perishable items and automatic waste reports.",
    "Export daily sales and low-stock reports to PDF/Excel directly from the app.",
])

# =====================================================================
# 15. REFERENCES
# =====================================================================
h1("14. References")
bullets([
    "Python 3 Official Documentation &mdash; docs.python.org (json, logging, unittest, re modules).",
    "VITyarthi &mdash; &quot;Build Your Own Project&quot;, General Project Instructions &amp; Submission Guidelines (course handout).",
    "Course lecture notes and lab exercises on functions, file handling, and exception handling (first-semester Python course).",
])

h1("15. Conclusion")
p("BakeryHub demonstrates how first-semester Python concepts &mdash; functions, "
  "dictionaries, file handling, exception handling, and basic OOP &mdash; can be "
  "combined into a modular, tested, real-world tool for a small business. It "
  "satisfies all functional and non-functional requirements set out in the "
  "project brief and provides a clear foundation for future enhancement.")

doc = SimpleDocTemplate(
    OUT_FILE, pagesize=A4,
    leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
    title="BakeryHub Project Report",
)
doc.build(story)
print(f"Report built at: {OUT_FILE}")
