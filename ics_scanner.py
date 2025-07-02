import socket
import ipaddress
import threading
from datetime import datetime

results = []
lock = threading.Lock()

ics_ports = {
    502: "Modbus",
    20000: "DNP3",
    44818: "EtherNet/IP",
    47808: "BACnet",
    1911: "Tridium Niagara"
}

def scan_ics_host(ip, port):
    try:
        with socket.create_connection((str(ip), port), timeout=3) as s:
            banner = s.recv(100).decode(errors="ignore")
            with lock:
                results.append({
                    "ip": str(ip),
                    "port": port,
                    "protocol": ics_ports.get(port, "Unknown"),
                    "banner": banner.strip(),
                    "timestamp": datetime.utcnow().isoformat()
                })
    except Exception:
        pass

def run_ics_scanner():
    print("\n--- ICS/SCADA Scanner ---")
    target = input("Enter target IP or CIDR range (e.g. 192.168.1.0/24): ").strip()

    try:
        net = ipaddress.ip_network(target, strict=False)
        threads = []

        for ip in net.hosts():
            for port in ics_ports:
                t = threading.Thread(target=scan_ics_host, args=(ip, port))
                t.start()
                threads.append(t)

        for t in threads:
            t.join()

        with open("ics_scan_results.txt", "w") as f:
            for r in results:
                f.write(str(r) + "\n")

        print("\n[+] ICS scan complete. Results saved to ics_scan_results.txt.")
    except Exception as e:
        print(f"[!] Error: {e}")

