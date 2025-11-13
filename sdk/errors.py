# sdk/errors.py
from functools import wraps

def mcp_safe(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            return {"ok": False, "error": {"code": "PLUGIN_ERROR", "message": str(e)}}
    return inner
