import unittest

from app.split import split


class SplitAcceptance(unittest.TestCase):
    def test_shares_add_up(self):
        self.assertEqual(sum(split(10, [1, 1, 1])), 10)
        self.assertEqual(len(split(10, [1, 1, 1])), 3)

    def test_exact_split(self):
        self.assertEqual(split(6, [1, 2]), [2, 4])

    def test_larger_remainder_wins(self):
        self.assertEqual(split(3, [5, 2]), [2, 1])

    def test_ties_go_to_earlier_weight(self):
        self.assertEqual(split(2, [1, 1, 1]), [1, 1, 0])

    def test_empty_weights(self):
        with self.assertRaises(ValueError):
            split(10, [])

    def test_negative_weight(self):
        with self.assertRaises(ValueError):
            split(10, [2, -1])

    def test_zero_weights(self):
        with self.assertRaises(ValueError):
            split(10, [0, 0])

    def test_negative_total(self):
        with self.assertRaises(ValueError):
            split(-1, [1])
