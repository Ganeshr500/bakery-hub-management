# Problem Statement

## Problem Statement
Small bakeries often track stock and sales using handwritten registers or
basic spreadsheets. This makes it easy to lose track of how much stock is
left, to accidentally sell more than what's actually available, and to
answer simple business questions like "what's our best-selling item?" or
"which items are about to run out?" There is a need for a simple, reliable,
script-based system — built using only core Python concepts learned in the
first semester — that keeps inventory and orders consistent and can
generate useful reports on demand.

## Scope of the Project
BakeryHub is a **single-location, console-based** application intended for
use by one bakery's staff/owner to manage their own inventory and orders.
Its scope includes:
- Maintaining a persistent catalogue of bakery items (ID, name, category,
  price, stock quantity).
- Processing customer orders: checking stock, deducting it, computing the
  bill, and recording the transaction.
- Cancelling orders and restoring the stock they had consumed.
- Producing low-stock alerts and sales analytics (revenue, best-sellers).

It is explicitly **out of scope** to provide: multi-branch/multi-location
support, a web or GUI interface, or online payment processing. Data is
persisted in a local SQLite database (`data/bakeryhub.db`) rather than a
separate database server, keeping the project self-contained and
dependency-free.

## Target Users
- **Primary user:** Bakery staff or the owner, who manages inventory and
  records orders at the counter.
- **Secondary/implicit users:** Customers, indirectly, as the people whose
  purchases are recorded and billed by the system.

## High-Level Features
1. **Inventory Management** — add, view, restock, update pricing for, and
   delete bakery items.
2. **Order Processing** — place a multi-item order with automatic stock
   validation and deduction, and cancel an order to restore stock.
3. **Reports & Analytics** — low-stock alerts, revenue summary (total
   revenue, average order value), and a best-selling items ranking.
4. Robust error handling, input validation, and activity logging throughout.
