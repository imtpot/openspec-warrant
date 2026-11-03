import unittest

from app.quota import check


class QuotaTest(unittest.TestCase):
    def test_fits(self):
        self.assertEqual(check(10, 4), 'fits')
