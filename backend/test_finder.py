"""
Checks finder.py against answer_key.csv (exported from the Answer_Key
tab of compass_care_milestone1.xlsx).

Run it with:
    python3 test_finder.py

For each of the 14 tests it re-runs find_nearest() with that test's
inputs and compares the output, site by site and distance by
distance, to what Excel produced. If every test passes, the Python
back end is doing exactly what the Excel workbook does.
"""

import csv
from collections import defaultdict

from finder import connect, find_nearest


def load_answer_key(path="answer_key.csv"):
    """Group the flat answer_key.csv rows back into one record per test."""
    tests = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            n = int(row["Test"])
            if n not in tests:
                tests[n] = {
                    "zip": row["ZIP"],
                    "site_group": row["Site group"],
                    "service": row["Service"],
                    "language": row["Language"],
                    "matches": int(float(row["Matches"])) if row["Matches"] else 0,
                    "message": row["Message"],
                    "results": [],
                }
            if row["Site key"]:
                tests[n]["results"].append({
                    "site_key": row["Site key"],
                    "name": row["Site name"],
                    "miles": float(row["Miles"]),
                    "result_type": row["Result type"],
                })
    return tests


def run_test(conn, n, test):
    got = find_nearest(
        conn, test["zip"],
        site_group=test["site_group"], service=test["service"], language=test["language"],
    )

    problems = []

    if got["matches"] != test["matches"]:
        problems.append(f"matches: expected {test['matches']}, got {got['matches']}")

    expected_msg = test["message"] or ("" if got["status"] == "OK" else got["status"])
    got_msg = got["message"] or ("" if got["status"] == "OK" else got["status"])
    if expected_msg != got_msg:
        problems.append(f"message: expected {expected_msg!r}, got {got_msg!r}")

    exp_keys = [r["site_key"] for r in test["results"]]
    got_keys = [s.site_key for s in got["results"]]
    if exp_keys != got_keys:
        problems.append(f"site order/identity: expected {exp_keys}, got {got_keys}")
    else:
        for exp, s in zip(test["results"], got["results"]):
            if abs(exp["miles"] - s.distance_miles) > 0.05:
                problems.append(f"{s.name}: expected {exp['miles']} mi, got {s.distance_miles} mi")
            if exp["result_type"] != s.result_type:
                problems.append(f"{s.name}: expected {exp['result_type']}, got {s.result_type}")

    label = f"ZIP {test['zip']:<6} {test['site_group']:<13} {test['service']:<14} {test['language']:<10}"
    if problems:
        print(f"  FAIL  test {n:>2}  {label}")
        for p in problems:
            print(f"          - {p}")
        return False
    else:
        print(f"  pass  test {n:>2}  {label}  ({got['matches']} match(es))")
        return True


def main():
    tests = load_answer_key()
    conn = connect()
    results = [run_test(conn, n, tests[n]) for n in sorted(tests)]
    conn.close()

    passed, total = sum(results), len(results)
    print(f"\n{passed}/{total} tests passed.")
    if passed < total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
