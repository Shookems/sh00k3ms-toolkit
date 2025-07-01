import requests
from bs4 import BeautifulSoup
import threading
import re
from datetime import datetime

results = []
lock = threading.Lock()

worker_patterns = [
    r"new\s+Worker\s*\(",
    r"new\s+SharedWorker\s*\(",
    r"navigator\.serviceWorker\.register"
]

def check_tech(url):
    try:
        resp = requests.get(url.strip(), timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        has_iframe = bool(soup.find_all("iframe"))
        scripts = soup.find_all("script")

        js_content = " ".join(s.text for s in scripts if s.string)
        has_worker = any(re.search(pat, js_content) for pat in worker_patterns)

        with lock:
            results.append({
                "url": url,
                "iframe_found": has_iframe,
                "web_worker_found": has_worker,
                "timestamp": datetime.utcnow().isoformat()
            })

        print(f"[+] {url} -> iframe: {has_iframe}, worker: {has_worker}")

    except Exception as e:
        with lock:
            results.append({
                "url": url,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
        print(f"[!] Error on {url}: {e}")

def run_iframe_worker_checker():
    print("\n--- Iframe & WebWorker Detector ---")
    urls = input("Enter comma-separated URLs: ").strip().split(",")
    urls = [u.strip() for u in urls if u]

    threads = []
    for url in urls:
        t = threading.Thread(target=check_tech, args=(url,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    with open("iframe_worker_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Analysis complete. Results saved to iframe_worker_results.txt.")

