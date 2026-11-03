def check(free, needed):
    """Return the verdict for one quota request."""
    if needed < 0:
        raise ValueError('needed must not be negative')
    if free >= needed:
        return 'fits'
    return None
