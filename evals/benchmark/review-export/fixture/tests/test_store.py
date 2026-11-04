import unittest

from app.store import find


class StoreTest(unittest.TestCase):
    def test_find(self):
        orders = [{'customer': 'a'}, {'customer': 'b'}]
        self.assertEqual(find(orders, 'a'), [{'customer': 'a'}])
