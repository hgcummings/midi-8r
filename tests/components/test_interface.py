from inspect import isclass
from pkgutil import iter_modules, walk_packages
from pathlib import Path
from importlib import import_module
import inspect


def has_method(cls, method_name):
    return any(
        name == method_name
        for name, _ in inspect.getmembers(cls, inspect.isfunction)
    )

def top_level_classes(module_name):
    module = import_module(module_name)
    return [
        attr for attr_name in dir(module)
        if isclass(attr := getattr(module, attr_name))
        and attr.__module__ == module_name
        and '.' not in attr.__qualname__
    ]

def components_dir():
    return Path(__file__.replace("tests", "src")).resolve().parent


def test_parameter_interface():
    params_pkg = import_module("src.components.params")
    for (_, name, is_pkg) in walk_packages(params_pkg.__path__, prefix=params_pkg.__name__ + '.'):
        if is_pkg:
            continue
        for cls in top_level_classes(name):
            print(cls)
            assert has_method(cls, "load")
            assert has_method(cls, "save")
            assert has_method(cls, "value_range")
            assert has_method(cls, "update_value")
            assert has_method(cls, "switch")
            assert has_method(cls, "has_changed")
            assert has_method(cls, "render")


def test_screen_interface():
    skip = {"colours"}
    for (_, name, is_pkg) in iter_modules([str(components_dir())]):
        if is_pkg or name in skip:
            continue
        module_name = f"src.components.{name}"
        for cls in top_level_classes(module_name):
            print(cls)
            assert has_method(cls, "set_nav")
            assert has_method(cls, "activate")
            assert has_method(cls, "update_value")
            assert has_method(cls, "switch")
            assert has_method(cls, "button_down")
            assert has_method(cls, "button_up")
