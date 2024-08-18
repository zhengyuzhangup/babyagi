import importlib


def can_import(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False