import os
import glob
import importlib

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
all_modules = [
    os.path.basename(f)[:-3]
    for f in modules
    if os.path.isfile(f)
    and not f.endswith("__init__.py")
    and not f.endswith("BaseSource.py")
]

for module in all_modules:
    importlib.import_module("JavPy.sources." + module)
