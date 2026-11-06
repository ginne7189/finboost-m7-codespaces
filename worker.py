"""로컬 이벤트 소비자. 클라우드 Lambda 실행을 대신 주장하지 않습니다."""

import argparse, json
from app import connect


def process(path):
    with connect(path) as con:
        con.execute("BEGIN IMMEDIATE")
        rows = con.execute("SELECT id,kind FROM events WHERE processed=0").fetchall()
        for r in rows:
            con.execute("UPDATE events SET processed=1 WHERE id=?", (r["id"],))
        # 교육에서는 외부 메일 등을 전송하지 않고 DB 안의 처리 상태만 바꿉니다.
        return {"processed_count": len(rows), "event_ids": [r["id"] for r in rows]}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--db", default="data/lab.db")
    a = p.parse_args()
    print(json.dumps(process(a.db), indent=2))
