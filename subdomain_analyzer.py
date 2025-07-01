import socket
import threading
from datetime import datetime

results = []
lock = threading.Lock()

# Wordlist (can expand later)
subdomains = [
    "www", "mail", "ftp", "admin", "api", "test", "dev", "portal", "secure",
    "web", "cpanel", "vpn", "beta", "stage", "staging", "m", "blog", "cdn",
    "img", "dashboard", "internal", "auth", "static", "files"
]

def resolve_subdomain(domain, sub):
    try:
        full = f"{sub}.{domain}"
        ip = socket.gethostbyname(full)
        with lock:
            results.append((full, ip))
            print(f"[+] Found: {full} -> {ip}")
    except socket.gaierror:
        pass

def run_subdomain_analyzer():
    print("\n--- Subdomain Analyzer ---")
    domain = input("Enter the target domain (e.g., example.com): ").strip()

    threads = []
    for sub in subdomains:
        t = threading.Thread(target=resolve_subdomain, args=(domain, sub))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    filename = "subdomain_results.txt"
    with open(filename, "w") as f:
        timestamp = datetime.utcnow().isoformat()
        for sub, ip in results:
            f.write(f"{sub} -> {ip} @ {timestamp}\n")

    print(f"\n[+] Subdomain scan complete. Results saved to {filename}")

