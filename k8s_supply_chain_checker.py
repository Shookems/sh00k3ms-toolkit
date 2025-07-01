import os
import re
from datetime import datetime

results = []

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, "r", errors="ignore") as f:
            content = f.read()

            if "latest" in content and ("image:" in content or "FROM" in content):
                findings.append("Unpinned 'latest' container image")

            if "privileged: true" in content:
                findings.append("Privileged pod/container config")

            if "capabilities:" in content and ("ALL" in content or "NET_ADMIN" in content):
                findings.append("Dangerous Linux capabilities")

            if "sysctls:" in content:
                findings.append("Use of custom sysctls")

            if "requirements.txt" in filepath:
                if re.search(r"==\s*$", content):
                    findings.append("Unpinned Python dependency")

            if "package.json" in filepath:
                if re.search(r"\"\^\d", content) or re.search(r"\"\~\d", content):
                    findings.append("Loosely pinned Node.js dependency")
    except Exception as e:
        findings.append(f"Error reading {filepath}: {str(e)}")

    return findings

def run_k8s_supply_chain_checker():
    print("\n--- K8s / Supply Chain Security Scanner ---")
    path = input("Enter file or directory to scan: ").strip()

    targets = []
    if os.path.isfile(path):
        targets = [path]
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                targets.append(os.path.join(root, file))
    else:
        print("[!] Invalid path.")
        return

    for file in targets:
        matches = scan_file(file)
        if matches:
            results.append({
                "file": file,
                "issues": matches,
                "timestamp": datetime.utcnow().isoformat()
            })

    with open("k8s_supply_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Scan complete. Results saved to k8s_supply_results.txt.")

