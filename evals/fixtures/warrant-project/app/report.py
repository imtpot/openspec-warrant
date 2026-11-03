def report(rows):
    """Print one line per row: name and value separated by a colon."""
    for name, value in rows:
        print(f'{name}: {value}')
