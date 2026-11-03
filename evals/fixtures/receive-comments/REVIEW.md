# Review comments on app/lookup.py

1. `lookup()` has no docstring. Add one that says what it returns.
2. Return exit code 0 for an unknown item as well; a missing item is not an error.
3. `lookup()` does not check for an empty name. Add a check.
4. The `main()` function looks off.
