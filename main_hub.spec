# -*- mode: python ; coding: utf-8 -*-
import ast
import os

ROOT = os.path.abspath(SPECPATH)

# Folders that should never be packed into the app
SKIP_DIRS = {"build", "dist", "app", "venv", "env", "node_modules", "__pycache__"}
# Loose files in the main folder that the games may need
KEEP_EXT = (".py", ".json", ".txt", ".csv", ".png", ".gif", ".jpg", ".jpeg",
            ".ico", ".wav", ".mp3", ".ogg", ".ttf")

datas = []
local_names = set()
py_files = []

for name in sorted(os.listdir(ROOT)):
    path = os.path.join(ROOT, name)
    if name.startswith(".") or name in SKIP_DIRS:
        continue
    if os.path.isdir(path):
        local_names.add(name)
        datas.append((path, name))
        for folder, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d != "__pycache__" and not d.startswith(".")]
            for f in files:
                if f.endswith(".py"):
                    py_files.append(os.path.join(folder, f))
    elif name != "main_hub.py" and name.lower().endswith(KEEP_EXT):
        datas.append((path, "."))
        if name.endswith(".py"):
            local_names.add(name[:-3])
            py_files.append(path)

# Find every library the game scripts import, so they get packed too
hidden = set()
for path in py_files:
    try:
        with open(path, encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
    except Exception:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                hidden.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            hidden.add(node.module)
            for alias in node.names:
                hidden.add(node.module + "." + alias.name)

hiddenimports = sorted(n for n in hidden if n.split(".")[0] not in local_names)

a = Analysis(
    ['main_hub.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main_hub',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main_hub',
)
