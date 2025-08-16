from __future__ import annotations
import logging
import requests

log = logging.getLogger("sh00k3ms.endpoint")

def _try(method: str, url: str, **kw):
    try:
        return requests.request(method, url, timeout=10, **kw)
    except Exception as e:
        log.debug("request %s %s failed: %s", method, url, e)
        return None

def run_endpoint_recon(url: str | None = None) -> None:
    """
    Quick endpoint recon:
      - HEAD for status/headers
      - GET robots.txt (if same origin)
      - OPTIONS to see allowed methods
      - GET for CSP/Server headers
    """
    if not url:
        print("Usage: sh00k3ms endpoint <url>")
        return

    print(f"[+] Probing {url}")
    r_head = _try("HEAD", url)
    if r_head is not None:
        print(f"STATUS: {r_head.status_code}")
        for k, v in sorted(r_head.headers.items()):
            if k.lower() in {"server", "x-powered-by", "content-type", "content-security-policy"}:
                print(f"{k}: {v}")

    # OPTIONS
    r_opt = _try("OPTIONS", url)
    if r_opt is not None and "allow" in r_opt.headers:
        print(f"ALLOW: {r_opt.headers.get('Allow')}")

    # GET main page
    r_get = _try("GET", url)
    if r_get is not None:
        for k in ("Server", "X-Powered-By", "Content-Security-Policy", "Strict-Transport-Security"):
            if k in r_get.headers:
                print(f"{k}: {r_get.headers[k]}")

    # robots.txt (same origin only)
    try:
        from urllib.parse import urlsplit, urlunsplit
        parts = urlsplit(url)
        robots = urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))
        r_robots = _try("GET", robots)
        if r_robots is not None and r_robots.ok:
            print("\n--- robots.txt ---")
            print(r_robots.text[:2000])  # avoid flooding
    except Exception as e:
        log.debug("robots fetch failed: %s", e)
