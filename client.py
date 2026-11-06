"""실제 HTTP 요청을 보내고 결과를 evidence/에 기록합니다."""

import argparse, json, os, urllib.request, urllib.error
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("action", choices=["health", "accounts", "transfer", "events"])
p.add_argument("--key", default="request-001")
p.add_argument("--amount", type=int, default=10000)
p.add_argument("--no-auth", action="store_true")
p.add_argument("--save")
p.add_argument("--base", default=os.environ.get("LAB_BASE_URL", "http://127.0.0.1:8000"))
a = p.parse_args()
headers = {}
if not a.no_auth:
    headers["Authorization"] = "Bearer " + os.environ.get(
        "LAB_TOKEN", "local-demo-only"
    )
body = None
endpoint = {
    "health": "/health",
    "accounts": "/v1/accounts",
    "events": "/v1/events",
    "transfer": "/v1/transfers",
}[a.action]
if a.action == "transfer":
    headers.update({"Content-Type": "application/json", "Idempotency-Key": a.key})
    body = json.dumps(
        {"from_account": "demo-a", "to_account": "demo-b", "amount_krw": a.amount}
    ).encode()
try:
    with urllib.request.urlopen(
        urllib.request.Request(a.base + endpoint, data=body, headers=headers), timeout=5
    ) as r:
        result = {"http_status": r.status, "body": json.load(r), "request_id": r.headers.get("X-Request-ID")}
except urllib.error.HTTPError as e:
    result = {"http_status": e.code, "body": json.load(e), "request_id": e.headers.get("X-Request-ID")}
except urllib.error.URLError as e:
    raise SystemExit("연결 실패: app.py 실행과 포트를 확인하세요. " + str(e.reason))
text = json.dumps(result, ensure_ascii=False, indent=2)
print(text)
if a.save:
    target = Path("evidence") / a.save
    if target.parent != Path("evidence") or target.suffix != ".json":
        raise SystemExit("--save는 파일명.json만 허용합니다.")
    target.parent.mkdir(exist_ok=True)
    target.write_text(text, encoding="utf-8")
