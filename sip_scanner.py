import socket
import threading
from datetime import datetime

results = []
lock = threading.Lock()

sip_ports = [5060]

def scan_sip_host(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(3)
            sip_probe = (
                f"OPTIONS sip:test@{ip} SIP/2.0\r\n"
                f"Via: SIP/2.0/UDP test.local;branch=z9hG4bK-1234\r\n"
                f"Max-Forwards: 70\r\n"
                f"To: <sip:test@{ip}>\r\n"
                f"From: fuzz <sip:fuzz@test.local>;tag=1234\r\n"
                f"Call-ID: 12345678@test.local\r\n"
                f"CSeq: 1 OPTIONS\r\n"
                f"Content-Length: 0\r\n\r\n"
            )
            s.sendto(sip_probe.encode(), (ip, port))
            response, _ = s.recvfrom(2048)
            banner = response.decode(errors="ignore")

            with lock:
                results.append({
                    "ip": ip,
                    "port": port,
                    "banner": banner.strip(),
                    "timestamp": datetime.utcnow().isoformat()
                })
    except Exception:
        pass

def run_sip_scanner():
    print("\n--- SIP Scanner ---")
    ips = input("Enter comma-separated IPs to scan for SIP (e.g. 10.0.0.1,10.0.0.2): ").strip().split(",")
    ips = [ip.strip() for ip in ips if ip.strip()]

    threads = []
    for ip in ips:
        for port in sip_ports:
            t = threading.Thread(target=scan_sip_host, args=(ip, port))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    with open("sip_scan_results.txt", "w") as f:
        for r in results:
            f.write(str(r) + "\n")

    print("\n[+] SIP scan complete. Results saved to sip_scan_results.txt.")

