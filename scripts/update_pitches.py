"""Update data/pitches.json with each pitch's result since the pitch price.

Runs daily from .github/workflows/pitch-tracker.yml. Standard library only.
Prices, dates, targets and stops come from the memos.

Closing rules, set before the outcome is known:
  1. Target hit: the first close at or beyond the memo target closes the pitch.
  2. Stop hit: the first close at or beyond the stop closes it (used for the
     short, where losses are not capped).
  3. Horizon: the pitch closes at the last close on or before its 12-month end.
  4. Manual: add "closed": {"date": "YYYY-MM-DD", "note": "..."} to a pitch
     when one of its memo's exit tests fails. That day's close is used.
A closed pitch keeps its final numbers; it is never removed.
"""
import datetime as dt
import json
import pathlib
import urllib.parse
import urllib.request

PITCHES = [
    {"key": "NKE",   "symbol": "NKE",    "side": "short", "ccy": "$", "price": 38.33,  "date": "2026-10-22",
     "target": 31.16, "stop": 47.88, "horizon_months": 12, "bench": "SPX"},
    {"key": "CPRT",  "symbol": "CPRT",   "side": "long",  "ccy": "$", "price": 27.59,  "date": "2026-09-25",
     "target": 37.30, "horizon_months": 12, "bench": "SPX"},
    {"key": "FTAI",  "symbol": "FTAI",   "side": "long",  "ccy": "$", "price": 169.97, "date": "2026-10-09",
     "target": 188.00, "horizon_months": 12, "bench": "SPX"},
    {"key": "SUMCO", "symbol": "3436.T", "side": "long",  "ccy": "¥", "price": 2053,   "date": "2026-04-10",
     "target": 3621, "horizon_months": 12, "bench": "TOPIX"},
]
BENCHMARKS = {
    "SPX":   {"symbol": "^GSPC",  "name": "S&P 500"},
    "TOPIX": {"symbol": "1306.T", "name": "TOPIX"},  # TOPIX ETF as a proxy for the index
}
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "pitches.json"


def history(symbol):
    """Daily closes for the past two years as a list of (date, close), oldest first."""
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
        if d > day:
            break
        best = (d, c)
    return best


def add_months(day, months):
    y, m = divmod(day.month - 1 + months, 12)
    y, m = day.year + y, m + 1
    for d in (day.day, 30, 29, 28):
        try:
            return dt.date(y, m, d)
        except ValueError:
            continue


def find_close(p, rows, start, end):
    """Decide whether and how the pitch has closed. Returns (date, price, reason) or None."""
    long = p["side"] == "long"
    if p.get("closed"):
        d, c = close_on_or_before(rows, dt.date.fromisoformat(p["closed"]["date"]))
        return d, c, "manual"
    stop = p.get("stop")
    for d, c in rows:
        if d <= start:
            continue
        if d > end:
            break
        if (long and c >= p["target"]) or (not long and c <= p["target"]):
            return d, c, "target"
        if stop is not None and ((long and c <= stop) or (not long and c >= stop)):
            return d, c, "stop"
    if rows[-1][0] >= end:
        d, c = close_on_or_before(rows, end)
        return d, c, "horizon"
    return None


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
        start = dt.date.fromisoformat(p["date"])
        end = add_months(start, p["horizon_months"])
        closed = find_close(p, rows, start, end)
        last_day, last = (closed[0], closed[1]) if closed else rows[-1]
        latest.append(rows[-1][0])

        ret = last / p["price"] - 1
        span = p["target"] - p["price"]
        progress = (last - p["price"]) / span if span else 0
        entry = {
            "side": p["side"],
            "ccy": p["ccy"],
            "start": {"date": p["date"], "price": p["price"]},
            "target": p["target"],
            "stop": p.get("stop"),
            "horizon_end": end.isoformat(),
            "last": {"date": last_day.isoformat(), "price": round(last, 2)},
            "return": round(ret, 4),
            # what the position made: a short gains when the stock falls
            "position": round(ret if p["side"] == "long" else -ret, 4),
            "progress": round(max(0.0, min(1.0, progress)), 4),
            "status": "closed" if closed else "open",
        }
        if closed:
            entry["closed"] = {"date": closed[0].isoformat(), "reason": closed[2],
                               "note": (p.get("closed") or {}).get("note")}

        b = BENCHMARKS[p["bench"]]
        brows = hist(b["symbol"])
        b_start = close_on_or_before(brows, start)
        b_end = close_on_or_before(brows, last_day)
        bret = b_end[1] / b_start[1] - 1
        entry["benchmark"] = {"name": b["name"], "return": round(bret, 4)}
        # a long beats the index if it rose more; a short wins if the stock lagged the index
        entry["relative"] = round((ret - bret) if p["side"] == "long" else (bret - ret), 4)
        out["pitches"][p["key"]] = entry
    out["updated"] = max(latest).isoformat()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
