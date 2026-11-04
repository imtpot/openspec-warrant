from app.store import find


def total(orders, customer):
    """Total cents a customer has spent."""
    return sum(int(o['cents']) for o in find(orders, customer))
