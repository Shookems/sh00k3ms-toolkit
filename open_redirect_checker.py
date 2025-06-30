import requests
import threading
from urllib.parse import urlencode
from datetime import datetime

results = []
lock = threading.Lock()

redirect_payloads = [
    "https://evil.com",
    "//evil.com",
    "///evil.com",
    "https://evil.com/%2F..",
    "/\\evil.com"
]

def test_redirect(url, param):
    for payload in redirect_payloads:
        test_params = {param: payload}
        try:
            resp = requests.get(url, params=test_params, allow_redirects=False, timeout=10)
            location = resp.headers.get("Location", "")
            if location and ("evil.com" in location or payload in location):
                with lock:
                    results.append({
                        "url": url,
                        "param": param,
                        "payload": payload,
                        "status": resp.status_code,
                        "location": location,
                        "timestamp": datetime.utcnow().isoformat()
                    })
                    print(f"[!] Possible open redirect at {url} with {payload}")
        except Exception as e:
            with lock:
                results.append({
                    "url": url,
                    "param": param,
                    "payload": payload,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })
            print(f"[!] Error testing {url} with {payload}: {e}")

def run_open_redirect_checker():
    print("\n--- Open Redirect Checker ---")
    urls = input("Enter comma-separated URLs: ").strip().split(",")
    urls = [u.strip() for u in urls if u]
    param = input("Enter redirect parameter to test (e.g., next, redirect, url): ").strip()

    threads = []
    for url in urls:
        t = threading.Thread(target=test_redirect, args=(url, param))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    with open("open_redirect_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Redirect testing complete. Results saved to open_redirect_results.txt.")

