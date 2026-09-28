"""
utils.py
--------
Cross-cutting helper functions: logger setup and input validation.
Separating these keeps validation logic testable and reusable across modules.
"""

import re
import logging
from config import LOG_FILE, CATEGORIES, MAX_UNIT_PRICE, MAX_ORDER_QTY
from exceptions import InvalidInputError

NAME_PATTERN = re.compile(r"^[A-Za-z0-9 ,.'&-]{2,60}$")
ITEM_ID_PATTERN = re.compile(r"^[A-Za-z0-9]{2,15}$")


def get_logger(name: str) -> logging.Logger:
    """
    Return a module-level logger that writes to logs/app.log.
    Using one logger factory keeps log formatting consistent (non-functional
    requirement: logging & monitoring).
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # avoid duplicate handlers on re-import
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def validate_item_id(item_id: str) -> str:
    item_id = item_id.strip().upper()
    if not ITEM_ID_PATTERN.match(item_id):
        raise InvalidInputError(
            "Item ID must be 2-15 alphanumeric characters (e.g. BR001)."
        )
    return item_id


def validate_item_name(name: str) -> str:
    name = name.strip()
    if not NAME_PATTERN.match(name):
        raise InvalidInputError(
            "Item name must be 2-60 characters (letters, numbers, spaces, & , . -)."
        )
    return name


def validate_category(category: str) -> str:
    category = category.strip().title()
    if category not in CATEGORIES:
        raise InvalidInputError(
            f"Category must be one of: {', '.join(CATEGORIES)}."
        )
    return category


def validate_price(value) -> float:
    try:
        price = float(value)
    except (TypeError, ValueError):
        raise InvalidInputError(f"Price must be numeric, got '{value}'.")
    if price <= 0 or price > MAX_UNIT_PRICE:
        raise InvalidInputError(
            f"Price must be between 0 and {MAX_UNIT_PRICE}, got {price}."
        )
    return round(price, 2)


def validate_quantity(value, allow_zero=False) -> int:
    try:
        qty = int(value)
    except (TypeError, ValueError):
        raise InvalidInputError(f"Quantity must be a whole number, got '{value}'.")
    lower_bound = 0 if allow_zero else 1
    if qty < lower_bound or qty > MAX_ORDER_QTY:
        raise InvalidInputError(
            f"Quantity must be between {lower_bound} and {MAX_ORDER_QTY}, got {qty}."
        )
    return qty


def validate_customer_name(name: str) -> str:
    name = name.strip()
    if not (2 <= len(name) <= 60):
        raise InvalidInputError("Customer name must be 2-60 characters.")
    return name
