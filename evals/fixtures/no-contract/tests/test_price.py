import unittest

from app.price import total


class TotalTest(unittest.TestCase):
    def test_applies_fractional_discount(self):
        self.assertEqual(total([50, 50], 0.1), 90)
