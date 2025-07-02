import socket
import ipaddress
import threading
from datetime import datetime

results = []
lock = threading.Lock()

iot_ports = {
    22: "SSH",
    23: "Telnet",
    80: "HTTP",
    443: "HTTPS",
    1900: "UPnP"
}

def scan_iot_host(ip, port):
    try:
        with socket.create_connection((str(ip), port), timeout=3) as s:
            banner = s.recv(100).decode(errors="ignore")
            with lock:
                results.append({
                    "ip": str(ip),
                    "port": port,
                    "protocol": iot_ports.get(port, "Unknown"),
                    "banner": banner.strip(),
                    "timestamp": datetime.utcnow().isoformat()
                })
    except Exception:
        pass

def run_iot_scanner():
    print("\n--- IoT Device Scanner ---")
    target = input("Enter target IP or CIDR range (e.g. 192.168.1.0/24): ").strip()

    try:
        net = ipaddress.ip_network(target, strict=False)
        threads = []

        for ip in net.hosts():
            for port in iot_ports:
                t = threading.Thread(target=scan_iot_host, args=(ip, port))
                t.start()
                threads.append(t)

        for t in threads:
            t.join()

        with open("iot_scan_results.txt", "w") as f:
            for r in results:
                f.write(str(r) + "\n")

        print("\n[+] IoT scan complete. Results saved to iot_scan_results.txt.")
    except Exception as e:
        print(f"[!] Error: {e}")

