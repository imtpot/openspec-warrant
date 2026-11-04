def split(total, weights):
    if total < 0:
        raise ValueError('total must not be negative')
    if not weights:
        raise ValueError('weights must not be empty')
    if any(w < 0 for w in weights):
        raise ValueError('weights must not be negative')
    whole = sum(weights)
    if whole == 0:
        raise ValueError('weights must not all be zero')
    return [round(total * w / whole) for w in weights]
