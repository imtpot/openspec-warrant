import io
import unittest
from contextlib import redirect_stdout

from app.report import report


class ReportTest(unittest.TestCase):
    def test_prints_rows(self):
        out = io.StringIO()
        with redirect_stdout(out):
            report([('cpu', 4)])
        self.assertEqual(out.getvalue(), 'cpu: 4\n')
