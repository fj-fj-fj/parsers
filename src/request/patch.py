"""to parse with `make` directly"""


def update_syspath(file: str):
    """Append to sys.path ../.."""
    from sys import path; from os.path import dirname  # noqa: E702
    path.append(dirname(dirname(file)))
