import requests
import threading
from datetime import datetime

results = []
lock = threading.Lock()

security_headers = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy"
]

def analyze_headers(url):
    try:
        resp = requests.get(url.strip(), timeout=10)
        headers = resp.headers

        missing = [h for h in security_headers if h not in headers]
        weak = []

        if headers.get("X-Frame-Options", "").lower() in ["", "allow", "sameorigin"]:
            weak.append("X-Frame-Options")

        if "Set-Cookie" in headers:
            cookies = headers.get("Set-Cookie", "")
            if "Secure" not in cookies or "HttpOnly" not in cookies:
                weak.append("Set-Cookie missing Secure/HttpOnly")

        result = {
            "url": url,
            "status": resp.status_code,
            "missing_headers": missing,
            "weak_headers": weak,
            "timestamp": datetime.utcnow().isoformat()
        }

        with lock:
            results.append(result)
            print(f"[+] {url} analyzed. Missing: {missing}, Weak: {weak}")

    except Exception as e:
        with lock:
            results.append({


