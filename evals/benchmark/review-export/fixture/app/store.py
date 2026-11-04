import csv


def load_orders(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def find(orders, customer):
    """Orders of one customer."""
    return [o for o in orders if o['customer'] == customer]
