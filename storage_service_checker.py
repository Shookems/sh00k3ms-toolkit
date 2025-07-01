import requests
from bs4 import BeautifulSoup
import threading
import re
from datetime import datetime

results = []
lock = threading.Lock()

storage_patterns = {
    "localStorage": r"localStorage",
    "sessionStorage": r"sessionStorage",
    "indexedDB": r"indexedDB",
    "serviceWorker": r"navigator\.serviceWorker\.register"
}

def check_storage_usage(url):
    try:
        resp = requests.get(url.strip(), timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        scripts = soup.find_all("script")
        js_content = " ".join(s.text for s in scripts if s.string)

        usage = {}
        for key, pattern in storage_patterns.items():
            usage[key] = bool(re.search(pattern, js_content))

        with lock:
            results.append({
                "url": url,
                "storage_usage": usage,
                "timestamp": datetime.utcnow().isoformat()
            })

        print(f"[+] {url} -> {usage}")

    except Exception as e:
        with lock:
            results.append({
                "url": url,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
        print(f"[!] Error on {url}: {e}")

def run_storage_service_checker():
    print("\n--- Storage & ServiceWorker Scanner ---")
    urls = input("Enter comma-separated URLs: ").strip().split(",")
    urls = [u.strip() for u in urls if u]

    threads = []
    for url in urls:
        t = threading.Thread(target=check_storage_usage, args=(url,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    with open("storage_service_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Scan complete. Results saved to storage_service_results.txt.")

