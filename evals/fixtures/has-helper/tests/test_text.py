import unittest

from app.text import slugify


class SlugifyTest(unittest.TestCase):
    def test_joins_lowercase_words(self):
        self.assertEqual(slugify('Quota Report  2026'), 'quota-report-2026')
