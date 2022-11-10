from types import SimpleNamespace

TARGET_BASE_URL = 'https://www.citilink.ru'
CPU = F'{TARGET_BASE_URL}/catalog/processory/'
MOTHERBOARD = F'{TARGET_BASE_URL}/materinskie-platy/'
RAM = F'{TARGET_BASE_URL}/moduli-pamyati/'
TARGET_ENDPOINTS = CPU, MOTHERBOARD, RAM


url = SimpleNamespace(
    base=TARGET_BASE_URL,
    cpu=CPU,
    mboard=MOTHERBOARD,
    ram=RAM,
    endpoints=lambda: TARGET_ENDPOINTS
)
