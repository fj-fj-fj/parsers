from multiprocessing.spawn import import_main_path

"""to parse with `make` directly"""


def update_syspath(file: str):
    """Append to sys.path ../.."""
    from sys import path; from os.path import dirname
    path.append(dirname(dirname(dirname(file))))
