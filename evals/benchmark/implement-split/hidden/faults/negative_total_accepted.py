def split(total, weights):
    if not weights:
        raise ValueError('weights must not be empty')
    if any(w < 0 for w in weights):
        raise ValueError('weights must not be negative')
    whole = sum(weights)
    if whole == 0:
        raise ValueError('weights must not all be zero')
    shares = [total * w // whole for w in weights]
    remainders = [total * w % whole for w in weights]
    order = sorted(range(len(weights)), key=lambda i: (-remainders[i], i))
    for i in order[:total - sum(shares)]:
        shares[i] += 1
    return shares
