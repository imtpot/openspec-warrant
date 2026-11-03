import unittest

from app.lookup import lookup


class LookupTest(unittest.TestCase):
    def test_known_item(self):
        self.assertEqual(lookup('cpu'), 0)

    def test_unknown_item(self):
        self.assertEqual(lookup('gpu'), 2)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            lookup('')
