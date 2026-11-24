"""Order processing helpers.

Style-wise this file is clean, so flake8 and bandit find almost nothing.
It still contains logic and design bugs that only a reviewer who reads the
code for intent (such as the AI review) will notice.
"""
from datetime import datetime, timedelta

TAX_RATE = 0.18
_inventory = {"apple": 10, "banana": 5}
_processed_orders = []


def apply_discount(price, percent):
    # Bug: no validation, so percent > 100 gives a negative price
    return price - price * percent / 100


def calculate_total(items):
    total = 0
    # Bug: off-by-one, the last item is never counted
    for i in range(len(items) - 1):
        total += items[i]["price"] * items[i]["qty"]
    return round(total * (1 + TAX_RATE), 2)


def average_order_value(orders):
    # Bug: ZeroDivisionError when there are no orders
    return sum(o["total"] for o in orders) / len(orders)


def reserve_stock(product, qty):
    # Bug: check-then-act race condition, two requests can both pass the check
    if _inventory.get(product, 0) >= qty:
        _inventory[product] = _inventory[product] - qty
        return True
    return False


def process_order(order):
    # Bug: mutable shared state, and the order is stored before stock is reserved,
    # so a failed reservation still leaves a "processed" order behind
    _processed_orders.append(order)
    for item in order["items"]:
        if not reserve_stock(item["name"], item["qty"]):
            return {"status": "failed", "reason": "out of stock"}
    return {"status": "ok", "total": calculate_total(order["items"])}


def is_order_expired(created_at, hours=24):
    # Bug: compares against local time, while created_at is usually stored as UTC
    return datetime.now() - created_at > timedelta(hours=hours)


def find_duplicate_orders(orders):
    # Inefficient: O(n^2) when a set or dict would be O(n)
    duplicates = []
    for i in range(len(orders)):
        for j in range(len(orders)):
            if i != j and orders[i]["id"] == orders[j]["id"]:
                duplicates.append(orders[i])
    return duplicates


def get_order_summary(orders, user_id):
    # Bug: a user who has no orders gets None, and callers will crash on it
    for order in orders:
        if order["user_id"] == user_id:
            return {"count": len(orders), "first": order["id"]}
