import unittest

from app.fetch import fetch_page


class FakeClient:
    def get(self, path):
        return path


class FetchTest(unittest.TestCase):
    def test_reads_first_page(self):
        self.assertEqual(fetch_page(FakeClient()), '/items?limit=100')
