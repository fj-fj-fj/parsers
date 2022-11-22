"""Module '_patch' for running this package directly."""


def update_syspath(file: str) -> None:
    """Append to sys.path ../.."""
    from sys import path; from os.path import dirname  # noqa: E702
    path.append(dirname(dirname(dirname(file))))
