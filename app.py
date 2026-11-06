"""교육용 가상 거래 API. 실거래/인터넷 공개 금지. Python 3.10+."""

import argparse, json, os, sqlite3, time, uuid
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def connect(path):
    con = sqlite3.connect(path, timeout=10)
    con.row_factory = sqlite3.Row
    return con


def init_db(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS accounts(id TEXT PRIMARY KEY,balance INTEGER NOT NULL CHECK(balance>=0));
        CREATE TABLE IF NOT EXISTS transfers(key TEXT PRIMARY KEY,payload TEXT NOT NULL,result TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY,kind TEXT NOT NULL,processed INTEGER NOT NULL DEFAULT 0);
        """)
        con.execute("INSERT OR IGNORE INTO accounts VALUES('demo-a',100000)")
        con.execute("INSERT OR IGNORE INTO accounts VALUES('demo-b',20000)")


def transfer(path, key, data):
    fields = {"from_account", "to_account", "amount_krw"}
    if not isinstance(data, dict) or set(data) != fields:
        return 400, {"error": "invalid_fields"}
    amount = data["amount_krw"]
    if type(amount) is not int or not 1 <= amount <= 1000000:
        return 400, {"error": "invalid_amount"}
    if not isinstance(key, str) or not 1 <= len(key) <= 80:
        return 400, {"error": "invalid_idempotency_key"}
    if any(not isinstance(data[k], str) for k in ("from_account", "to_account")):
        return 400, {"error": "invalid_account"}
    if data["from_account"] == data["to_account"]:
        return 400, {"error": "same_account"}
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    with connect(path) as con:
        # 잔액과 처리 키를 같은 트랜잭션에 저장합니다.
        con.execute("BEGIN IMMEDIATE")
        old = con.execute("SELECT * FROM transfers WHERE key=?", (key,)).fetchone()
        if old:
            if old["payload"] != canonical:
                return 409, {"error": "key_conflict"}
            return 200, {**json.loads(old["result"]), "replayed": True}
        a = con.execute(
            "SELECT balance FROM accounts WHERE id=?", (data["from_account"],)
        ).fetchone()
        b = con.execute(
            "SELECT balance FROM accounts WHERE id=?", (data["to_account"],)
        ).fetchone()
        if a is None or b is None:
            return 404, {"error": "account_not_found"}
        if a["balance"] < amount:
            return 422, {"error": "insufficient_funds"}
        con.execute(
            "UPDATE accounts SET balance=balance-? WHERE id=?",
            (amount, data["from_account"]),
        )
        con.execute(
            "UPDATE accounts SET balance=balance+? WHERE id=?",
            (amount, data["to_account"]),
        )
        tid = str(uuid.uuid4())
        result = {
            "transfer_id": tid,
            "status": "accepted",
            "amount_krw": amount,
            "replayed": False,
        }
        con.execute(
            "INSERT INTO transfers VALUES(?,?,?)", (key, canonical, json.dumps(result))
        )
        con.execute("INSERT INTO events(id,kind) VALUES(?,'transfer.accepted')", (tid,))
        return 201, result


def make_server(path, port=8000, host="127.0.0.1"):
    token = os.environ.get("LAB_TOKEN", "local-demo-only")

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, status, body):
            request_id = str(uuid.uuid4())
            payload = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("X-Request-ID", request_id)
            self.end_headers()
            self.wfile.write(payload)
            print(
                json.dumps(
                    {
                        "request_id": request_id,
                        "path": self.path.split("?", 1)[0],
                        "transfer_id": body.get("transfer_id"),
                        "error": body.get("error"),
                        "method": self.command,
                        "status": status,
                    }
                ),
                flush=True,
            )

        def auth(self):
            if self.headers.get("Authorization") != "Bearer " + token:
                self.reply(401, {"error": "unauthorized"})
                return False
            return True

        def do_GET(self):
            if self.path == "/health":
                return self.reply(200, {"status": "ok", "mode": "local-training"})
            if not self.auth():
                return
            with connect(path) as con:
                if self.path == "/v1/accounts":
                    return self.reply(
                        200,
                        {
                            "accounts": [
                                dict(x)
                                for x in con.execute(
                                    "SELECT * FROM accounts ORDER BY id"
                                )
                            ]
                        },
                    )
                if self.path == "/v1/events":
                    return self.reply(
                        200,
                        {
                            "events": [
                                dict(x)
                                for x in con.execute("SELECT * FROM events ORDER BY id")
                            ]
                        },
                    )
            self.reply(404, {"error": "not_found"})

        def do_POST(self):
            if not self.auth():
                return
            if self.path != "/v1/transfers":
                return self.reply(404, {"error": "not_found"})
            try:
                n = int(self.headers.get("Content-Length", "0"))
                if n < 1 or n > 4096:
                    return self.reply(400, {"error": "invalid_body_size"})
                data = json.loads(self.rfile.read(n))
            except (ValueError, UnicodeDecodeError):
                return self.reply(400, {"error": "invalid_json"})
            try:
                status, result = transfer(
                    path, self.headers.get("Idempotency-Key"), data
                )
            except sqlite3.OperationalError:
                return self.reply(503, {"error": "database_busy"})
            self.reply(status, result)

    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--db", default=os.environ.get("LAB_DB_PATH", "data/lab.db"))
    p.add_argument("--port", type=int, default=int(os.environ.get("LAB_PORT", "8000")))
    p.add_argument("--host", default=os.environ.get("LAB_HOST", "127.0.0.1"))
    a = p.parse_args()
    init_db(a.db)
    print("Local training server ready", flush=True)
    try:
        make_server(a.db, a.port, a.host).serve_forever()
    except KeyboardInterrupt:
        pass
