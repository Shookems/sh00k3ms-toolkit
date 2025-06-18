
import os
import requests
import subprocess
import shutil
from dotenv import load_dotenv

load_dotenv()

SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
NVD_API_KEY = os.getenv("NVD_API_KEY")
TESTSSL_PATH = shutil.which("testssl.sh")

def banner():
    print("\n=== TLS Checker ===")
    print("1. Basic TLS Version + Cipher")
    print("2. Run testssl.sh Scan")
    print("3. Shodan TLS Recon")
    print("4. NVD CVE Lookup")
    print("0. Exit")

def get_target():
    return input("\nEnter the domain or IP to scan: ").strip()

def output_file(name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"tls_{name}_{timestamp}.txt"

def check_tls_basic(target):
    import ssl, socket
    context = ssl.create_default_context()
    try:
        with socket.create_connection((target, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                print(f"[+] TLS Version: {ssock.version()}")
                print(f"[+] Cipher: {ssock.cipher()}")
    except Exception as e:
        print(f"[!] TLS connection failed: {e}")

def run_testssl(target):
    if not TESTSSL_PATH:
        print("[-] testssl.sh is not installed or not in PATH.")
        return
    outfile = output_file("testssl")
    print(f"[+] Running testssl.sh against {target}...")
    with open(outfile, "w") as f:
        subprocess.run([TESTSSL_PATH, "--fast", target], stdout=f, stderr=subprocess.STDOUT)
    print(f"[+] Output saved to {outfile}")

def run_shodan_tls(target):
    if not SHODAN_API_KEY:
        print("[-] Missing SHODAN_API_KEY.")
        return
    ip = target.split(":")[0]
    url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
    print(f"[+] Querying Shodan for {ip}...")
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        for item in data.get("data", []):
            if "ssl" in item:
                print(f"→ Port {item.get('port')}: TLS {item['ssl'].get('version')}")
                print(f"   Cipher: {item['ssl'].get('cipher')} | Cert: {item['ssl'].get('cert', {}).get('subject')}")
    except Exception as e:
        print(f"[!] Shodan error: {e}")

def run_nvd_lookup():
    if not NVD_API_KEY:
        print("[-] Missing NVD_API_KEY.")
        return
    keyword = input("Enter TLS version or keyword to search CVEs (e.g., TLS 1.0, RC4): ").strip()
    headers = {"apiKey": NVD_API_KEY}
    params = {"keywordSearch": keyword, "resultsPerPage": 5}
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    print(f"[+] Searching NVD for: {keyword}")
    try:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        for item in r.json().get("vulnerabilities", []):
            cve = item["cve"]
            print(f"→ {cve['id']}: {cve['descriptions'][0]['value']}")
    except Exception as e:
        print(f"[!] NVD lookup error: {e}")

def run_tls_checker():
    while True:
        banner()
        choice = input("Select an option: ").strip()
        if choice == "1":
            check_tls_basic(get_target())
        elif choice == "2":
            run_testssl(get_target())
        elif choice == "3":
            run_shodan_tls(get_target())
        elif choice == "4":
            run_nvd_lookup()
        elif choice == "0":
            break
        else:
            print("Invalid option.")
