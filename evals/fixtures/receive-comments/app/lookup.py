import sys

ITEMS = {'cpu', 'ram'}


def lookup(name, items=ITEMS):
    if not name:
        raise ValueError('name required')
    if name in items:
        return 0
    return 2


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    return lookup(args[0] if args else '')
