# Builds main, a bare origin and a feature branch with the refund change.
set -e
G='git -c user.name=fixture -c user.email=fixture@invalid'
git branch -M main
rm -f setup.sh
git add -A
$G commit -q --amend --no-edit
git clone -q --bare . .git/origin.git
git remote add origin "$PWD/.git/origin.git"
git fetch -q origin
git remote set-head origin main >/dev/null
git checkout -q -b feature
cat > app/dates.py <<'PY'
from datetime import date


def days_between(start: date, end: date, include_end: bool = True) -> int:
    """Days from `start` to `end`; `end` counts unless include_end is False."""
    return (end - start).days + (1 if include_end else 0)
PY
cat > app/refund.py <<'PY'
import os
from datetime import date

from app.dates import days_between

EXPORTS = 'exports'


def refund_amount(amount: int, cancel: date, period_start: date, period_end: date, currency: str = 'EUR') -> int:
    if cancel < period_start:
        return amount
    unused = days_between(cancel, period_end, include_end=False)
    period = days_between(period_start, period_end, include_end=False)
    return round(amount * unused / period)


def export_refund(name: str, cents: int) -> None:
    os.makedirs(EXPORTS, exist_ok=True)
    with open(os.path.join(EXPORTS, name), 'w') as f:
        f.write(str(cents))
PY
cat > tests/test_refund.py <<'PY'
import unittest
from datetime import date

from app.refund import refund_amount


class RefundTest(unittest.TestCase):
    def test_half_of_april(self):
        expected = refund_amount(3000, date(2026, 4, 16), date(2026, 4, 1), date(2026, 5, 1))
        self.assertEqual(refund_amount(3000, date(2026, 4, 16), date(2026, 4, 1), date(2026, 5, 1)), expected)
PY
git add -A
$G commit -q -m 'Add refunds'
