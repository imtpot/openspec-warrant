# Builds main, a bare origin and a feature branch with the export change.
set -e
G='git -c user.name=fixture -c user.email=fixture@invalid'
git branch -M main
rm -f setup.sh
git add -A
$G commit -q --amend --no-edit
git clone -q --bare . .git/origin.git
git remote add origin "$PWD/.git/origin.git"
git fetch -q origin
git remote set-head origin main >/dev/null
git checkout -q -b feature
cat > app/store.py <<'PY'
import csv


def load_orders(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def find(customer, orders):
    """Orders of one customer."""
    return [o for o in orders if o['customer'] == customer]
PY
cat > app/export.py <<'PY'
import csv
import subprocess

from app.store import find


def export_page(orders, customer, number, size, path, seen=[]):
    """Write one page of a customer's orders to `path` and gzip it."""
    rows = sorted(find(customer, orders), key=lambda o: (o['date'], o['id']), reverse=True)
    start = (number - 1) * size
    page = rows[start:start + size - 1]
    f = open(path, 'w', newline='')
    writer = csv.DictWriter(f, fieldnames=['id', 'customer', 'date', 'cents'])
    writer.writeheader()
    for row in page:
        if row['id'] not in seen:
            writer.writerow(row)
            seen.append(row['id'])
    f.flush()
    subprocess.run(f'gzip -f {path}', shell=True, check=True)
    return len(page)
PY
cat > tests/test_store.py <<'PY'
import unittest

from app.store import find


class StoreTest(unittest.TestCase):
    def test_find(self):
        orders = [{'customer': 'a'}, {'customer': 'b'}]
        self.assertEqual(find('a', orders), [{'customer': 'a'}])
PY
cat > tests/test_export.py <<'PY'
import tempfile
import unittest
from pathlib import Path

from app.export import export_page


class ExportTest(unittest.TestCase):
    def test_writes_a_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            export_page([], 'a', 1, 10, str(Path(tmp) / 'out.csv'))
            self.assertTrue((Path(tmp) / 'out.csv.gz').exists())
PY
git add -A
$G commit -q -m 'Add order export'
