import module
from exchange import Exchange


def get_exchange_by_name(name):
    exchanges = get_available_exchanges()
    exchange = module.get_module_by_name(name, exchanges)
    return exchange() if exchange else None


def get_available_exchanges():
    return module.get_available_modules('exchanges', Exchange, __file__)
