from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module

import inspect

def has_method(type, method_name):
    matching_members = [member for name, member in inspect.getmembers(type, inspect.isfunction) if name == method_name]
    return len(matching_members) == 1

def test_interface():
    package_dir = Path(__file__.replace("tests", "src")).resolve().parent
    for (_, module_name, _) in iter_modules([package_dir]):

        # import the module and iterate through its attributes
        module = import_module(f"src.components.{module_name}")
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if isclass(attribute) and attribute.__module__.startswith("src.components"):
                print(attribute)
                assert has_method(attribute, "load")
                assert has_method(attribute, "save")                
                assert has_method(attribute, "show_view")
                assert has_method(attribute, "edit")
                assert has_method(attribute, "update_value")
                assert has_method(attribute, "switch")
                assert has_method(attribute, "next")
