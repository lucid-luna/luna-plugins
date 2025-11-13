# sdk/config.py
import json, os
from pathlib import Path
from typing import Any, Dict

def load_config(plugin_key: str) -> Dict[str, Any]:
    cfg_root = Path(__file__).resolve().parent.parent / "config"
    env_blob = os.environ.get(f"LUNA_PLUGIN_{plugin_key.upper()}_CONFIG")
    if env_blob:
        try:
            return json.loads(env_blob)
        except Exception:
            pass
    for name in ("config.json", "config_example.json"):
        p = cfg_root / name
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                return data.get(plugin_key, {})
            except Exception:
                continue
    return {}
