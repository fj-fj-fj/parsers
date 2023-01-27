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
Ip = str
Port = str | int
Proxy = str
Proxies = list[Proxy]


def collect_proxy(ip: Ip, port: Port) -> Proxy:
    return f'{ip}:{port}'


def collect_proxies(ips: list[Ip], ports: list[Port]) -> Proxies:
    return [collect_proxy(ip, port) for ip, port in zip(ips, ports)]


def main(samples: list) -> Proxies:
    """Handle samples. (API)"""
    return collect_proxies(*samples)
