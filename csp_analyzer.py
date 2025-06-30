import requests
import threading
from datetime import datetime

results = []
lock = threading.Lock()

dangerous_keywords = [
    "*", "unsafe-inline", "unsafe-eval", "data:", "blob:", "filesystem:"
]

def parse_csp(csp_value):
    issues = []
    directives = csp_value.split(";")
    for directive in directives:
        parts = directive.strip().split()
        if not parts:
            continue
        name, *sources = parts
        for src in sources:
            if src in dangerous_keywords:
                issues.append(f"{name}: {src}")
    return issues

def analyze_csp(url):
    try:
        resp = requests.get(url.strip(), timeout=10)
        csp = resp.headers.get("Content-Security-Policy")
        if csp:
            issues = parse_csp(csp)
            result = {
                "url": url,
                "status": resp.status_code,
                "csp_present": True,
                "csp_issues": issues,
                "timestamp": datetime.utcnow().isoformat()
            }
            print(f"[+] {url} - CSP issues: {issues if issues else 'None'}")
        else:
            result = {
                "url": url,
                "status": resp.status_code,
                "csp_present": False,
                "csp_issues": ["Missing CSP header"],
                "timestamp": datetime.utcnow().isoformat()
            }
            print(f"[!] {url} - Missing CSP header")

        with lock:
            results.append(result)

    except Exception as e:
        with lock:
            results.append({
                "url": url,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
        print(f"[!] Error analyzing {url}: {e}")

def run_csp_analyzer():
    print("\n--- Content-Security-Policy (CSP) Analyzer ---")
    urls = input("Enter comma-separated URLs: ").strip().split(",")
    urls = [u.strip() for u in urls if u]

    threads = []
    for url in urls:
        t = threading.Thread(target=analyze_csp, args=(url,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    with open("csp_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] CSP analysis complete. Results saved to csp_results.txt.")

