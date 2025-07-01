import json
import os
from datetime import datetime

results = []

escalation_actions = [
    "iam:CreatePolicyVersion",
    "iam:PutUserPolicy",
    "iam:AttachUserPolicy",
    "iam:PassRole",
    "sts:AssumeRole",
    "lambda:CreateFunction",
    "iam:UpdateAssumeRolePolicy",
    "iam:CreateAccessKey",
    "iam:CreateLoginProfile"
]

def analyze_policy(file_path):
    try:
        with open(file_path, "r") as f:
            policy = json.load(f)
    except Exception as e:
        return [{"error": f"Could not read policy: {e}"}]

    matches = []
    statements = policy.get("Statement", [])
    if not isinstance(statements, list):
        statements = [statements]

    for stmt in statements:
        actions = stmt.get("Action", [])
        if isinstance(actions, str):
            actions = [actions]

        for action in actions:
            for esc_action in escalation_actions:
                if esc_action.lower() in action.lower() or action == "*" or "iam:*" in action.lower():
                    matches.append({
                        "statement": stmt,
                        "escalation_action": esc_action
                    })

    return matches

def run_aws_priv_esc_analyzer():
    print("\n--- AWS Privilege Escalation Analyzer ---")
    file_path = input("Enter path to IAM policy JSON file: ").strip()

    if not os.path.isfile(file_path):
        print("[!] File not found.")
        return

    matches = analyze_policy(file_path)

    if matches:
        results.append({
            "file": file_path,
            "findings": matches,
            "timestamp": datetime.utcnow().isoformat()
        })

        with open("aws_priv_esc_results.txt", "w") as f:
            for r in results:
                f.write(str(r) + "\n")

        print("\n[+] Privilege escalation risks found. Results saved to aws_priv_esc_results.txt.")
    else:
        print("[+] No privilege escalation patterns found.")

