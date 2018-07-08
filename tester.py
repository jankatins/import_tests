import sys
import os
import os.path
import importlib

what = ''
try:
    what = sys.argv[1]
except:
	pass

if what == 'script':
    path = os.path.dirname(sys.argv[0])
else:
    path = 'without'

app_module_name = 'app.app'

print(sys.path)

try:
	importlib.import_module(app_module_name)
	print("!! Found app.app module already importable without sys.path manipulation")
	sys.exit(0)
except ModuleNotFoundError:
	pass

def try_import_at(path):
    if not os.path.exists(path):
        return None
    inserted = False
    if sys.path[0] != path:
        sys.path.insert(0, path)
        inserted = True
    try:
        print(f"* Trying import with {path} in sys.path")
        app = importlib.import_module(app_module_name)
        return app
    except ModuleNotFoundError:
        if inserted:
            del sys.path[0]
        return None

path = os.path.abspath(path)
print(f"Trying {path} and parents to find app.app module")
while path:
    app = try_import_at(path)
    if app:
        print(f"!! Found app.app module in {path}")
        sys.exit(0)
    path, name = os.path.split(path)
    if not name:
        break
print("!! Not found app.app module!")
