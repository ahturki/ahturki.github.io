"""Update data/pitches.json with each pitch's move since the pitch price.

Runs daily from .github/workflows/pitch-tracker.yml. Standard library only.
Pitch prices and dates come from the memos. A pitch with no date gets no
benchmark comparison (its own return is still computed from the memo price).
"""
import datetime as dt
import json
import pathlib
import urllib.parse
import urllib.request

PITCHES = [
    # key, Yahoo symbol, side, pitch price (from memo), price date (from memo), benchmark
    {"key": "NKE",   "symbol": "NKE",    "side": "short", "price": 38.33,  "date": "2026-10-22", "bench": "SPX"},
    {"key": "CPRT",  "symbol": "CPRT",   "side": "long",  "price": 27.59,  "date": "2026-09-25", "bench": "SPX"},
    {"key": "FTAI",  "symbol": "FTAI",   "side": "long",  "price": 169.97, "date": "2026-10-09", "bench": "SPX"},
    {"key": "SUMCO", "symbol": "3436.T", "side": "long",  "price": 2053,   "date": "2026-04-10", "bench": "TOPIX"},
]
BENCHMARKS = {
    "SPX":   {"symbol": "^GSPC",  "name": "S&P 500"},
    "TOPIX": {"symbol": "1306.T", "name": "TOPIX"},  # TOPIX ETF as a proxy for the index
}
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "pitches.json"


def history(symbol):
    """Daily closes for the past two years as a list of (date, close)."""
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           f"{urllib.parse.quote(symbol)}?range=2y&interval=1d")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (pitch-tracker)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)["chart"]["result"][0]
    tz = res["meta"]["gmtoffset"]
    closes = res["indicators"]["quote"][0]["close"]
    rows = []
    for t, c in zip(res.get("timestamp") or [], closes):
        if c is not None:
            day = dt.datetime.fromtimestamp(t + tz, dt.timezone.utc).date()
            rows.append((day, float(c)))
    return rows


def close_on_or_before(rows, day):
    """Close on the given day, or the last trading day before it."""
    best = None
    for d, c in rows:
        if d <= day:
            best = (d, c)
        else:
            break
    return best


def main():
    cache = {}

    def hist(sym):
        if sym not in cache:
            cache[sym] = history(sym)
        return cache[sym]

    out = {"updated": None, "pitches": {}}
    latest = []
    for p in PITCHES:
        rows = hist(p["symbol"])
        last_day, last = rows[-1]
        latest.append(last_day)
        ret = last / p["price"] - 1
        entry = {
            "side": p["side"],
            "start": {"date": p["date"], "price": p["price"]},
            "last": {"date": last_day.isoformat(), "price": round(last, 2)},
            "return": round(ret, 4),
            # what the position made: a short gains when the stock falls
            "position": round(ret if p["side"] == "long" else -ret, 4),
        }
        if p["date"]:
            b = BENCHMARKS[p["bench"]]
            brows = hist(b["symbol"])
            start = close_on_or_before(brows, dt.date.fromisoformat(p["date"]))
            b_last_day, b_last = brows[-1]
            bret = b_last / start[1] - 1
            entry["benchmark"] = {"name": b["name"], "return": round(bret, 4)}
            # relative call: long beats the index if it rose more; short wins if it lagged the index
            rel = (ret - bret) if p["side"] == "long" else (bret - ret)
            entry["relative"] = round(rel, 4)
        out["pitches"][p["key"]] = entry
    out["updated"] = max(latest).isoformat()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
