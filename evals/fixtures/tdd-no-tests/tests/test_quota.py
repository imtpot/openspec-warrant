import unittest

from app.quota import check


class QuotaTest(unittest.TestCase):
    # Fits verdict: Enough free
    def test_enough_free(self):
        self.assertEqual(check(10, 4), 'fits')
