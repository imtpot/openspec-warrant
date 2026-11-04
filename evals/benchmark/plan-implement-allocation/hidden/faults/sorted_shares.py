def allocate(total_cents, percents):
    if not percents:
        raise ValueError('percents must not be empty')
    if any(p < 0 for p in percents) or sum(percents) != 100:
        raise ValueError('percents must be non-negative and add up to 100')
    if total_cents < 0:
        raise ValueError('total must not be negative')
    shares = [total_cents * p // 100 for p in percents]
    remainders = [total_cents * p % 100 for p in percents]
    order = sorted(range(len(percents)), key=lambda i: (-remainders[i], i))
    for i in order[:total_cents - sum(shares)]:
        shares[i] += 1
    return sorted(shares)
