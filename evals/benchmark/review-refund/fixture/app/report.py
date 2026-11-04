from app.dates import days_between


def billed_days(start, end):
    """Days billed for [start, end): the end day is not billed."""
    return days_between(start, end)
