def slugify(title):
    """Return the URL slug of a title: lowercase words joined by hyphens."""
    return '-'.join(title.lower().split())
