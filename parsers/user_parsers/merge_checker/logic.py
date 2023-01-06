"""Module contains sample processing logic.

Example:

    >>> def main(samples):
    ...    return [f'{ip}:{port}' for ip,port in zip(*samples)]
    ...
    >>> ips = ['140.82.121.4', '140.82.121.4']
    >>> ports = ['80', '443']
    >>> main([ips, ports])
    ['140.82.121.4:80', '140.82.121.4:443']

"""
from typing import Any


def main(samples: list[Any]) -> list[Any]:
    """Handle samples. (API)"""
