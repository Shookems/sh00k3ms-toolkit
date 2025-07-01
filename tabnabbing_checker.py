import requests
from bs4 import BeautifulSoup
import threading
from datetime import datetime

results = []
lock = threading.Lock()

def check_tabnabbing(url):
    try:
        resp = requests.get(url.strip(), timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        atags = soup.find_all("a", target="_blank")

        for a in atags:
            rel = a.get("rel", [])
            if not rel or ("noopener" not in rel and "noreferrer" not in rel):
                with lock:
                    results.append({
                        "url": url,
                        "href": a.get("href"),
                        "text": a.text.strip(),
                        "issue": "Missing rel=noopener/noreferrer",
                        "timestamp": datetime.utcnow().isoformat()
                    })
    except Exception as e:
        with lock:
            results.append({
                "url": url,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })

def run_tabnabbing_checker():
    print("\n--- Tabnabbing Checker ---")
    urls = input("Enter comma-separated URLs: ").strip().split(",")
    urls = [u.strip() for u in urls if u]

    threads = []
    for url in urls:
        t = threading.Thread(target=check_tabnabbing, args=(url,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    with open("tabnabbing_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Tabnabbing check complete. Results saved to tabnabbing_results.txt.")

