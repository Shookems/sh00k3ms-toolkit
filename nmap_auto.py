import subprocess
import threading
import re
from datetime import datetime

def is_valid_target(target):
    # Basic IP or domain name validation
    ip_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
    domain_pattern = re.compile(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return bool(ip_pattern.match(target) or domain_pattern.match(target))

def run_nmap_scan(target, flags, output_prefix):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    sanitized = re.sub(r'\W+', '_', target)
    output_file = f"{output_prefix}_{sanitized}_{timestamp}.txt"

    try:
        print(f"[+] Scanning {target} with flags: {flags}")
        result = subprocess.run(
            ["nmap"] + flags.split() + [target],
            capture_output=True, text=True, timeout=300
        )
        with open(output_file, "w") as f:
            f.write(result.stdout)
        print(f"[+] Scan complete. Output saved to: {output_file}")
    except Exception as e:
        print(f"[!] Error scanning {target}: {e}")

def run_nmap_scanner():
    print("\n--- Automated Nmap Scan Tool ---")
    targets = input("Enter comma-separated IPs/domains: ").strip().split(",")
    targets = [t.strip() for t in targets if is_valid_target(t.strip())]

    if not targets:
        print("[!] No valid targets provided.")
        return

    flags = input("Enter Nmap flags (default: -sC -sV -Pn): ").strip()
    if not flags:
        flags = "-sC -sV -Pn"

    prefix = input("Enter output file prefix (e.g., 'scan'): ").strip()
    if not prefix:
        prefix = "scan"

    threads = []
    for target in targets:
        t = threading.Thread(target=run_nmap_scan, args=(target, flags, prefix))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("[+] All scans completed.")

