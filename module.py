import os
import importlib
import inspect


def get_module_by_name(name, modules):
    try:
        return list(filter(lambda s: s['name'].lower() == name.lower(), modules))[0]['class']
    except (IndexError, AttributeError):
        pass


def get_available_modules(python_package, entity_type, loader_module_file,
                          exclude_modules=['__init__.py', 'loader.py']):
    items = []
    modules = filter(lambda m: m not in exclude_modules and m.endswith('.py'),
                     os.listdir(os.path.dirname(loader_module_file)))

    for mod in modules:
        module_name = importlib.import_module(f'{python_package}.{mod[:-3]}')
        module_classes = map(lambda c: c[1], inspect.getmembers(module_name, inspect.isclass))
        try:
            strategy = list(filter(lambda c: not c == entity_type and issubclass(c, entity_type), module_classes))[-1]
            items.append({
                'name': mod[:-3],
                'class': strategy
            })
        except IndexError:
            del module_name

    return items
