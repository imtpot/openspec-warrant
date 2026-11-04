import unittest
from datetime import date

from app.billing import days_between, monthly_price


class BillingTest(unittest.TestCase):
    def test_monthly_price_per_seat(self):
        self.assertEqual(monthly_price('team', 3), 14700)

    def test_unknown_plan(self):
        with self.assertRaises(ValueError):
            monthly_price('gold')

    def test_days_between_excludes_end(self):
        self.assertEqual(days_between(date(2026, 1, 1), date(2026, 1, 31)), 30)
