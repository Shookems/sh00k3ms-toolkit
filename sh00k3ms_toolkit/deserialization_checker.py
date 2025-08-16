from __future__ import annotations
import logging
import re
import requests
import yaml

log = logging.getLogger("sh00k3ms.deser")

DANGEROUS_YAML_TOKENS = (
    r"!!python/object",
    r"!!python/object/new",
    r"!!python/module",
    r"!!python/name",
)

PHP_SERIALIZED_RE = re.compile(r"""(^|[^A-Za-z])([aObisdN]:\d+:.+;)""", re.IGNORECASE)

def run_deserialization_checker(target: str | None = None) -> None:
    """
    Heuristics:
      - Fetch target (URL) and look for common serialized patterns (PHP)
      - If YAML-looking, warn on dangerous tags (we still parse with safe_load)
    """
    if not target:
        print("Usage: sh00k3ms deser <url>")
        return

    print(f"[+] Fetching {target}")
    try:
        resp = requests.get(target, timeout=10)
    except Exception as e:
        log.error("request failed: %s", e)
        return

    text = resp.text or ""
    # PHP serialized blobs (very rough heuristic)
    if PHP_SERIALIZED_RE.search(text):
        print("[!] Potential PHP-serialized payload detected in response")

    # YAML heuristics
    if any(t in text for t in ("---", ": ", "\n- ")):
        if any(tok in text for tok in DANGEROUS_YAML_TOKENS):
            print("[!] Potentially dangerous YAML tags observed (code execution risk)")
        try:
            yaml.safe_load(text)
            print("[+] YAML safe_load(): no exception")
        except Exception as e:
            print(f"[?] YAML safe_load() raised: {e}")
