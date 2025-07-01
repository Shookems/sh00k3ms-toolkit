import socket
import requests
import threading
from datetime import datetime

results = []
lock = threading.Lock()

cdn_signatures = {
    "Cloudflare": ["cloudflare", "cf-ray", "cf-cache-status"],
    "Akamai": ["akamai", "akamai-cache-status"],
    "Fastly": ["fastly", "x-served-by"],
    "Amazon CloudFront": ["cloudfront", "x-amz-cf-id"],
    "Google Cloud CDN": ["x-goog-", "google"],
    "Azure CDN": ["azurecdn", "x-azure-ref"]
}

def analyze_domain(domain):
    result = {
        "domain": domain,
        "ip": None,
        "cdn": None,
        "headers": {},
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        ip = socket.gethostbyname(domain)
        result["ip"] = ip

        resp = requests.get(f"http://{domain}", timeout=10)
        headers = resp.headers
        result["headers"] = dict(headers)

        for cdn, markers in cdn_signatures.items():
            if any(marker.lower() in str(headers).lower() for marker in markers):
                result["cdn"] = cdn
                break

        with lock:
            results.append(result)
            print(f"[+] {domain} -> CDN: {result['cdn'] or 'None'}")

    except Exception as e:
        result["error"] = str(e)
        with lock:
            results.append(result)
            print(f"[!] Error analyzing {domain}: {e}")

def run_cdn_edge_mapper():
    print("\n--- CDN Edge Mapper ---")
    domains = input("Enter comma-separated domains (e.g., example.com,www.site.com): ").strip().split(",")
    domains = [d.strip() for d in domains if d.strip()]

    threads = []
    for domain in domains:
        t = threading.Thread(target=analyze_domain, args=(domain,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    with open("cdn_edge_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] CDN mapping complete. Results saved to cdn_edge_results.txt.")

