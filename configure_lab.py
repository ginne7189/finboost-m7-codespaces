"""Create or inspect training Compose settings without displaying secret values."""
import argparse, json, subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--init", action="store_true")
p.add_argument("--port", type=int)
p.add_argument("--check", action="store_true")
a = p.parse_args()
if a.port is not None and not 1024 <= a.port <= 65535:
    p.error("Port must be between 1024 and 65535")
target = Path(".env")
if not target.exists():
    if not a.init:
        p.error("Run python configure_lab.py --init first")
    target.write_text(Path(".env.example").read_text(encoding="utf-8"), encoding="utf-8")
    print("Created .env from the training example")
else:
    print("Kept existing .env")
if a.port is not None:
    lines = target.read_text(encoding="utf-8").splitlines()
    lines = [line for line in lines if not line.startswith("LAB_HOST_PORT=")]
    lines.append(f"LAB_HOST_PORT={a.port}")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"LAB_HOST_PORT={a.port}")
if a.check:
    try:
        result = subprocess.run(["docker", "compose", "--profile", "tools", "config", "--format", "json"], capture_output=True, text=True)
        if result.returncode:
            p.error("Compose config failed. Check Docker Compose and required .env values. No configuration values were printed.")
        config = json.loads(result.stdout)
        api = config["services"]["api"]
        client = config["services"]["client"]
        api_env, client_env = api["environment"], client["environment"]
        db = api_env["LAB_DB_PATH"]
        if not db.startswith("/app/data/") or ".." in db.split("/"):
            p.error("LAB_DB_PATH must stay below /app/data/ so the mounted volume retains it")
        if not api_env.get("LAB_TOKEN") or api_env["LAB_TOKEN"] != client_env.get("LAB_TOKEN"):
            p.error("API and client need the same nonempty training token")
        port = api["ports"][0]
        if port.get("host_ip") != "127.0.0.1":
            p.error("Training API must bind the host port to 127.0.0.1")
        print("PASS: token mapping, DB mount path and loopback binding")
        print("Effective host port:", port["published"])
        print("NOTE: shell environment may override .env; this is the resolved Compose setting")
    except (OSError, KeyError, ValueError):
        p.error("Cannot inspect Compose config; verify Docker Compose v2 and compose.yaml")
print("Host Python does not automatically load .env.")
