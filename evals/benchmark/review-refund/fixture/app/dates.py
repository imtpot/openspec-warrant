from datetime import date


def days_between(start: date, end: date, include_end: bool = False) -> int:
    """Days from `start` to `end`; `end` counts only with include_end."""
    return (end - start).days + (1 if include_end else 0)
