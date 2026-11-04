"""
Runs the same 14 Answer_Key tests as test_finder.py, but through the
running API over real HTTP requests instead of calling find_nearest()
directly. This checks the whole path: URL -> api.py -> finder.py ->
compass_care.db -> JSON response.

Start the server first:
    uvicorn api:app --port 8008
Then run:
    python3 test_api.py
"""

import csv
import urllib.parse
import urllib.request
import json

BASE_URL = "http://127.0.0.1:8008"


def load_answer_key(path="answer_key.csv"):
    tests = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            n = int(row["Test"])
            if n not in tests:
                tests[n] = {
                    "zip": row["ZIP"], "site_group": row["Site group"],
                    "service": row["Service"], "language": row["Language"],
                    "matches": int(float(row["Matches"])) if row["Matches"] else 0,
                    "results": [],
                }
            if row["Site key"]:
                tests[n]["results"].append({
                    "site_key": row["Site key"], "name": row["Site name"],
                    "miles": float(row["Miles"]), "result_type": row["Result type"],
                })
    return tests


def call_api(test):
    params = urllib.parse.urlencode({
        "zip": test["zip"], "site_group": test["site_group"],
        "service": test["service"], "language": test["language"],
    })
    with urllib.request.urlopen(f"{BASE_URL}/sites?{params}") as resp:
        return json.load(resp)


def run_test(n, test):
    got = call_api(test)
    problems = []

    if got["matches"] != test["matches"]:
        problems.append(f"matches: expected {test['matches']}, got {got['matches']}")

    exp_keys = [r["site_key"] for r in test["results"]]
    got_keys = [r["site_key"] for r in got["results"]]
    if exp_keys != got_keys:
        problems.append(f"site order/identity: expected {exp_keys}, got {got_keys}")
    else:
        for exp, r in zip(test["results"], got["results"]):
            if abs(exp["miles"] - r["distance_miles"]) > 0.05:
                problems.append(f"{r['name']}: expected {exp['miles']} mi, got {r['distance_miles']} mi")
            if exp["result_type"] != r["result_type"]:
                problems.append(f"{r['name']}: expected {exp['result_type']}, got {r['result_type']}")

    label = f"ZIP {test['zip']:<6} {test['site_group']:<13} {test['service']:<14} {test['language']:<10}"
    if problems:
        print(f"  FAIL  test {n:>2}  {label}")
        for p in problems:
            print(f"          - {p}")
        return False
    print(f"  pass  test {n:>2}  {label}  ({got['matches']} match(es))")
    return True


def main():
    tests = load_answer_key()
    results = [run_test(n, tests[n]) for n in sorted(tests)]
    passed, total = sum(results), len(results)
    print(f"\n{passed}/{total} tests passed (via the live API).")
    if passed < total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
