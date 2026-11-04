import unittest
from datetime import date as d

from app.billing import prorate

APRIL = (d(2026, 4, 1), d(2026, 5, 1))


class ProrationAcceptance(unittest.TestCase):
    def test_half_period(self):
        self.assertEqual(prorate(3000, d(2026, 4, 16), d(2026, 5, 1), *APRIL), 1500)

    def test_february_length(self):
        self.assertEqual(prorate(2800, d(2026, 2, 1), d(2026, 2, 15), d(2026, 2, 1), d(2026, 3, 1)), 1400)

    def test_rounds_two_thirds_up(self):
        self.assertEqual(prorate(1000, d(2026, 4, 11), d(2026, 5, 1), *APRIL), 667)

    def test_exact_half_cent_rounds_up(self):
        self.assertEqual(prorate(1, d(2026, 4, 16), d(2026, 5, 1), *APRIL), 1)

    def test_start_before_period(self):
        self.assertEqual(prorate(3000, d(2026, 3, 20), d(2026, 4, 16), *APRIL), 1500)

    def test_end_after_period(self):
        self.assertEqual(prorate(3000, d(2026, 4, 16), d(2026, 6, 1), *APRIL), 1500)

    def test_no_overlap_before(self):
        self.assertEqual(prorate(3000, d(2026, 3, 1), d(2026, 3, 10), *APRIL), 0)

    def test_no_overlap_after(self):
        self.assertEqual(prorate(3000, d(2026, 5, 10), d(2026, 5, 20), *APRIL), 0)

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            prorate(-100, *APRIL, *APRIL)

    def test_swapped_period(self):
        with self.assertRaises(ValueError):
            prorate(3000, *APRIL, d(2026, 5, 1), d(2026, 4, 1))

    def test_empty_period(self):
        with self.assertRaises(ValueError):
            prorate(3000, *APRIL, d(2026, 4, 1), d(2026, 4, 1))
