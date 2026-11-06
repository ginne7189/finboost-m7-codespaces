"""FinBoost local environment check. Does not start a server or send data."""

import argparse, platform, socket, sys, tempfile
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--port", type=int, default=8000)
a = p.parse_args()
folder = Path.cwd()
required = ["app.py", "client.py", "worker.py", "test_app.py"]
ok = True
version = sys.version_info
print("ENV: Local computer / " + platform.system())
print("PYTHON:", platform.python_version())
if version[:2] == (3, 14):
    print("PASS: Course Python 3.14 selected")
else:
    print(
        "CHECK: Course instructions use Python 3.14. Select that version before continuing."
    )
    ok = False
print("FOLDER:", folder)
missing = [n for n in required if not (folder / n).is_file()]
if missing:
    print("FAIL: Missing files:", ", ".join(missing))
    ok = False
else:
    print("PASS: app.py / client.py / worker.py / test_app.py found")
try:
    with tempfile.TemporaryFile(dir=folder) as f:
        f.write(b"finboost-write-check")
        f.flush()
    print("PASS: Folder is writable")
except OSError as e:
    print("FAIL: Folder is not writable:", str(e))
    ok = False
with socket.socket() as s:
    s.settimeout(0.5)
    busy = s.connect_ex(("127.0.0.1", a.port)) == 0
if busy:
    print(
        "CHECK: Port",
        a.port,
        "already responds. Check whether your lab server is running.",
    )
    ok = False
else:
    print("PASS: Port", a.port, "has no listening server (check for this moment only)")
if (folder / "data/lab.db").exists():
    print("NOTE: Existing lab.db found. Balances may reflect an earlier practice.")
else:
    print("NOTE: First server start will create data/lab.db.")
print(
    "READY: Start Terminal A, then send requests from Terminal B."
    if ok
    else "NOT READY: Resolve the checks above first."
)
sys.exit(0 if ok else 1)
