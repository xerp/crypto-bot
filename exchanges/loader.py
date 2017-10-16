import os
import inspect
import importlib

from exchange import Exchange


def get_exchange_by_name(name):
    exchanges = get_available_exchanges()

    try:
        return list(filter(lambda e: e.name.lower() == name.lower(), exchanges))[0]
    except (IndexError, AttributeError):
        pass


def get_available_exchanges():
    exchanges = []
    exchange_package = 'exchanges'
    exclude_modules = ['__init__.py', 'loader.py']
    modules = filter(lambda m: m not in exclude_modules and m.endswith('.py'),
                     os.listdir(os.path.dirname(__file__)))

    for mod in modules:
        module_name = importlib.import_module(f'{exchange_package}.{mod[:-3]}')
        module_classes = map(lambda c: c[1], inspect.getmembers(module_name, inspect.isclass))
        try:
            exchange = list(filter(lambda c: not c == Exchange and issubclass(c, Exchange), module_classes))[0]
            exchanges.append(exchange())
        except IndexError:
            del module_name

    return exchanges
