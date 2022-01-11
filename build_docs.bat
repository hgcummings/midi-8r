rd /s /q docs

set PYTHONPATH=";%CD%\\src;%CD%\\tools\\stubs;"

pdoc --html -o docs components core ports adapters