def split(total, weights):
    if total < 0:
        raise ValueError('total must not be negative')
    if not weights:
        raise ValueError('weights must not be empty')
    whole = sum(weights)
    if whole == 0:
        raise ValueError('weights must not all be zero')
    shares = [total * w // whole for w in weights]
    remainders = [total * w % whole for w in weights]
    order = sorted(range(len(weights)), key=lambda i: (-remainders[i], i))
    for i in order[:total - sum(shares)]:
        shares[i] += 1
    return shares
