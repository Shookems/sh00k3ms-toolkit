import json
import os
from datetime import datetime

results = []

def analyze_azure_file(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        return [{"error": f"Unable to read file: {e}"}]

    output = {
        "tenantId": data.get("tenantId"),
        "subscriptionId": data.get("id"),
        "displayName": data.get("displayName"),
        "domain": data.get("user", {}).get("name", "").split("@")[-1] if data.get("user") else None,
        "timestamp": datetime.utcnow().isoformat()
    }

    return [output]

def run_azure_security_tools():
    print("\n--- Azure Security Analyzer ---")
    file_path = input("Enter path to Azure account JSON file (e.g., from `az account show`): ").strip()

    if not os.path.isfile(file_path):
        print("[!] File not found.")
        return

    analysis = analyze_azure_file(file_path)
    results.extend(analysis)

    with open("azure_security_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Azure analysis complete. Results saved to azure_security_results.txt.")

