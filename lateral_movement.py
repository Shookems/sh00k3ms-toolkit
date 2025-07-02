import socket
import threading
from datetime import datetime

results = []
lock = threading.Lock()

lateral_ports = {
    445: "SMB",
    135: "RPC",
    139: "NetBIOS",
    3389: "RDP",
    389: "LDAP",
    5985: "WinRM (HTTP)",
    5986: "WinRM (HTTPS)"
}

def scan_lateral_host(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=3):
            with lock:
                results.append({
                    "ip": ip,
                    "port": port,
                    "service": lateral_ports.get(port, "Unknown"),
                    "timestamp": datetime.utcnow().isoformat()
                })
    except:
        pass

def run_lateral_movement():
    print("\n--- Lateral Movement Scanner ---")
    targets = input("Enter comma-separated IPs to scan (e.g. 10.0.0.1,10.0.0.2): ").strip().split(",")
    ip_list = [ip.strip() for ip in targets if ip.strip()]

    threads = []
    for ip in ip_list:
        for port in lateral_ports:
            t = threading.Thread(target=scan_lateral_host, args=(ip, port))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    with open("lateral_movement_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] Lateral movement scan complete. Results saved to lateral_movement_results.txt.")

