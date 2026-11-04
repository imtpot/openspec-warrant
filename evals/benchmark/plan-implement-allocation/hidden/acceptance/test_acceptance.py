import unittest

from app.allocation import allocate


class AllocationAcceptance(unittest.TestCase):
    def test_exact_split(self):
        self.assertEqual(allocate(1000, [50, 30, 20]), [500, 300, 200])

    def test_keeps_the_order_of_the_percentages(self):
        self.assertEqual(allocate(1000, [20, 50, 30]), [200, 500, 300])

    def test_shares_add_up_to_the_total(self):
        self.assertEqual(sum(allocate(10, [33, 33, 34])), 10)

    def test_each_share_within_one_cent(self):
        for share in allocate(7, [25, 25, 25, 25]):
            self.assertIn(share, (1, 2))

    def test_zero_total(self):
        self.assertEqual(allocate(0, [60, 40]), [0, 0])

    def test_single_cost_center(self):
        self.assertEqual(allocate(999, [100]), [999])
