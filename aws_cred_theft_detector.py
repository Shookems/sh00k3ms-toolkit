import os
import re
from datetime import datetime

results = []

patterns = {
    "AWS_ACCESS_KEY_ID": r"AKIA[0-9A-Z]{16}",
    "AWS_SECRET_ACCESS_KEY": r"(?<![A-Z0-9])[A-Za-z0-9/+=]{40}(?![A-Z0-9])",
    "AWS_SESSION_TOKEN": r"Fwo[A-Za-z0-9/+=]{80,}"
}

def scan_file_for_creds(file_path):
    findings = []
    try:
        with open(file_path, "r", errors="ignore") as f:
            content = f.read()
            for name, regex in patterns.items():
                matches = re.findall(regex, content)
                if matches:
                    findings.append((name, matches))
    except Exception as e:
        findings.append(("ERROR", [str(e)]))
    return findings

def run_aws_cred_theft_detector():
    print("\n--- AWS Credential Theft Detector ---")
    path = input("Enter file or directory path to scan: ").strip()

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

    for filepath in targets:
        matches = scan_file_for_creds(filepath)
        if matches:
            results.append({
                "file": filepath,
                "matches": matches,
                "timestamp": datetime.utcnow().isoformat()
            })

    with open("aws_cred_theft_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Scan complete. Results saved to aws_cred_theft_results.txt.")


