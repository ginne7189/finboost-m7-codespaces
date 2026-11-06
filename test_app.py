import unittest, tempfile, threading, json, os, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from app import init_db, transfer, connect, make_server
from worker import process


class LabTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = self.tmp.name + "/lab.db"
        init_db(self.db)
        self.body = {
            "from_account": "demo-a",
            "to_account": "demo-b",
            "amount_krw": 10000,
        }

    def tearDown(self):
        self.tmp.cleanup()

    def balances(self):
        with connect(self.db) as c:
            return [
                x["balance"] for x in c.execute("SELECT * FROM accounts ORDER BY id")
            ]

    def test_success(self):
        self.assertEqual(transfer(self.db, "a", self.body)[0], 201)
        self.assertEqual(self.balances(), [90000, 30000])

    def test_replay(self):
        first = transfer(self.db, "a", self.body)[1]
        s, r = transfer(self.db, "a", self.body)
        self.assertEqual(s, 200)
        self.assertEqual(r["transfer_id"], first["transfer_id"])
        self.assertTrue(r["replayed"])
        self.assertEqual(self.balances(), [90000, 30000])

    def test_conflict(self):
        transfer(self.db, "a", self.body)
        self.assertEqual(transfer(self.db, "a", {**self.body, "amount_krw": 1})[0], 409)

    def test_insufficient(self):
        self.assertEqual(
            transfer(self.db, "a", {**self.body, "amount_krw": 100001})[0], 422
        )
        self.assertEqual(self.balances(), [100000, 20000])

    def test_invalid_amounts(self):
        for n in [0, -1, True, 1.2, "10000", 1000001]:
            self.assertEqual(
                transfer(self.db, "a", {**self.body, "amount_krw": n})[0], 400
            )

    def test_missing_account(self):
        self.assertEqual(
            transfer(self.db, "a", {**self.body, "to_account": "absent"})[0], 404
        )

    def test_missing_key(self):
        self.assertEqual(transfer(self.db, None, self.body)[0], 400)

    def test_restart_persistence(self):
        transfer(self.db, "a", self.body)
        init_db(self.db)
        self.assertEqual(transfer(self.db, "a", self.body)[0], 200)

    def test_concurrent_replay(self):
        with ThreadPoolExecutor(4) as pool:
            codes = list(
                pool.map(lambda _: transfer(self.db, "a", self.body)[0], range(4))
            )
        self.assertEqual(codes.count(201), 1)
        self.assertEqual(codes.count(200), 3)
        self.assertEqual(self.balances(), [90000, 30000])

    def test_worker_replay(self):
        transfer(self.db, "a", self.body)
        self.assertEqual(process(self.db)["processed_count"], 1)
        self.assertEqual(process(self.db)["processed_count"], 0)

    def test_http_auth_json_paths(self):
        server = make_server(self.db, 0)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        base = "http://127.0.0.1:" + str(server.server_port)
        try:
            with urllib.request.urlopen(base + "/health") as r:
                self.assertEqual(r.status, 200)
            with self.assertRaises(urllib.error.HTTPError) as e:
                urllib.request.urlopen(base + "/v1/accounts")
            self.assertEqual(e.exception.code, 401)
            token = os.environ.get("LAB_TOKEN", "local-demo-only")
            req = urllib.request.Request(
                base + "/v1/transfers",
                data=b"{bad",
                headers={"Authorization": "Bearer " + token},
            )
            with self.assertRaises(urllib.error.HTTPError) as e:
                urllib.request.urlopen(req)
            self.assertEqual(e.exception.code, 400)
        finally:
            server.shutdown()
            server.server_close()
            t.join()


if __name__ == "__main__":
    unittest.main(verbosity=2)
