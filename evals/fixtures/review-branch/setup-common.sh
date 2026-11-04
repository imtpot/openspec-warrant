# Sourced by the setup-*.sh scripts with VARIANT set to feature, empty,
# no-change or two-changes. Builds main, a bare origin and a feature branch.
set -e
G='git -c user.name=fixture -c user.email=fixture@invalid'
git branch -M main
rm -f setup-*.sh
case "$VARIANT" in
  no-change) rm -rf openspec/changes/add-quota-check ;;
  two-changes) cp -R openspec/changes/add-quota-check openspec/changes/add-quota-report ;;
esac
git add -A
$G commit -q --amend --no-edit
$G tag v0.1.0
git clone -q --bare . .git/origin.git
git remote add origin "$PWD/.git/origin.git"
git fetch -q origin
git remote set-head origin main >/dev/null
git checkout -q -b feature
[ "$VARIANT" = empty ] && exit 0
cat > app/quota.py <<'PY'
def check(free, needed, retries=3):
    """Return the verdict for one quota request."""
    if free >= needed:
        return 'fits'
    return 'short'


def formatReport(result):
    return f'verdict: {result}'
PY
cat > app/cli.py <<'PY'
import argparse
import json

from app.quota import check, formatReport


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('free', type=int)
    parser.add_argument('needed', type=int)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    result = check(args.needed, args.free)
    print(json.dumps({'verdict': result}) if args.json else formatReport(result))
PY
git add -A
$G commit -q -m 'Add shortfall verdict and command line'
