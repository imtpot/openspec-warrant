from pathlib import Path


def safe_path(base: Path, name: str) -> Path:
    """`base / name`, refusing names that leave `base`."""
    path = (base / name).resolve()
    if not path.is_relative_to(base.resolve()):
        raise ValueError(f'path leaves {base}: {name}')
    return path
