import unittest

from app.quota import free_capacity


class FreeTest(unittest.TestCase):
    def test_free(self):
        self.assertEqual(free_capacity(10, 4), 6)
