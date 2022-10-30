"""Contains files, URLs, xpath etc."""

from types import SimpleNamespace


const = SimpleNamespace(
    FILE_PARSED_PROXIES='request/proxy/parsed_data/proxies',
    FILE_RESPONSE='request/proxy/log/response.html',

    URL='https://free-proxy-list.net/',

    SELECT_IP='td:nth-of-type(1)',
    SELECT_PORT='td:nth-of-type(2)',
)
