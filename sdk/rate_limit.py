# sdk/rate_limit.py
import time
from functools import wraps

def limit(rate: str):
    num, per = rate.split("/")
    num = int(num); window = {"s":1, "m":60, "h":3600}[per[0]]
    bucket = {"count": 0, "start": 0.0}
    def deco(fn):
        @wraps(fn)
        def inner(*a, **kw):
            now = time.time()
            if now - bucket["start"] > window:
                bucket["start"] = now; bucket["count"] = 0
            if bucket["count"] >= num:
                return {"ok": False, "error": {"code": "RATE_LIMIT", "message": f"{rate}"}}
            bucket["count"] += 1
            return fn(*a, **kw)
        return inner
    return deco
