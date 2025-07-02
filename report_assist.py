from datetime import datetime

results = []

# Expanded static mapping: OWASP Top 10 + common issues
expanded_db = {
    "xss": {
        "stride": "Tampering",
        "cwe": "CWE-79: Cross-site Scripting",
        "cvss": "6.1"
    },
    "sqli": {
        "stride": "Tampering",
        "cwe": "CWE-89: SQL Injection",
        "cvss": "8.8"
    },
    "idOR": {
        "stride": "Information Disclosure",
        "cwe": "CWE-639: IDOR",
        "cvss": "7.5"
    },
    "ssrf": {
        "stride": "Information Disclosure",
        "cwe": "CWE-918: SSRF",
        "cvss": "8.2"
    },
    "unvalidated redirect": {
        "stride": "Spoofing",
        "cwe": "CWE-601: Open Redirect",
        "cvss": "6.1"
    },
    "excessive permissions": {
        "stride": "Elevation of Privilege",
        "cwe": "CWE-732: Incorrect Permission Assignment",
        "cvss": "7.4"
    },
    "missing logging": {
        "stride": "Repudiation",
        "cwe": "CWE-778: Insufficient Logging",
        "cvss": "6.5"
    },
    "debug": {
        "stride": "Information Disclosure",
        "cwe": "CWE-215: Information Exposure Through Debug Info",
        "cvss": "5.3"
    },
    "deserialization": {
        "stride": "Elevation of Privilege",
        "cwe": "CWE-502: Unsafe Deserialization",
        "cvss": "8.0"
    }
}

def prompt_cvss_override(metric, default):
    val = input(f"{metric} [{default}]: ").strip().upper()
    return val if val else default

def run_report_assist():
    print("\n--- Report Assist (Upgraded) ---")
    finding = input("Enter vulnerability description or title: ").strip().lower()

    matched = None
    for keyword, details in expanded_db.items():
        if keyword in finding:
            matched = details
            break

    if matched:
        print(f"\n[+] STRIDE: {matched['stride']}")
        print(f"[+] CWE: {matched['cwe']}")
        print(f"[+] CVSS Base Score: {matched['cvss']}")
        use_manual = input("Would you like to manually score CVSS? (y/N): ").strip().lower() == "y"
    else:
        print("\n[!] No exact match found — entering manual mode.")
        use_manual = True
        matched = {
            "stride": input("STRIDE category: ").strip(),
            "cwe": input("CWE ID and name: ").strip()
        }

    if use_manual:
        print("\n--- CVSS 3.1 Scoring ---")
        base_vector = {
            "AV": prompt_cvss_override("Attack Vector (AV) [N/A/L/P]", "N"),
            "AC": prompt_cvss_override("Attack Complexity (AC) [L/H]", "L"),
            "PR": prompt_cvss_override("Privileges Required (PR) [N/L/H]", "L"),
            "UI": prompt_cvss_override("User Interaction (UI) [N/R]", "N"),
            "S": prompt_cvss_override("Scope (S) [U/C]", "U"),
            "C": prompt_cvss_override("Confidentiality Impact (C) [N/L/H]", "H"),
            "I": prompt_cvss_override("Integrity Impact (I) [N/L/H]", "H"),
            "A": prompt_cvss_override("Availability Impact (A) [N/L/H]", "H"),
        }
        matched["cvss"] = f"CVSS:3.1/{'/'.join(f'{k}:{v}' for k, v in base_vector.items())}"

    result = {
        "description": finding,
        "stride": matched["stride"],
        "cwe": matched["cwe"],
        "cvss": matched["cvss"],
        "timestamp": datetime.utcnow().isoformat()
    }

    results.append(result)

    with open("report_assist_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Report assist complete. Results saved to report_assist_results.txt.")

