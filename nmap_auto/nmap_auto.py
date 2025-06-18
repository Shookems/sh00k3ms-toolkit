import subprocess
import shutil
import os
import sys

def run_nmap(targets, scan_type, output_file):
    for target in targets:
        print(f"\n[+] Running Nmap against {target} ({scan_type.upper()} scan)...")
        if scan_type == "tcp":
            cmd = ["nmap", "-p-", "-sS", "-A", "-T5", "-oN", f"{output_file}_tcp.txt", target]
        else:
            cmd = ["nmap", "-sU", "-T5", "-oN", f"{output_file}_udp.txt", target]

        if ("-sU" in cmd or "-sS" in cmd) and os.geteuid() != 0:
            print("\n[!] This scan type requires root privileges. Please run with sudo.\n")
            return

        if not shutil.which("nmap"):
            print("Error: Nmap is not installed or not in your PATH.")
            return

        subprocess.run(cmd)

def get_targets():
    targets = input("Enter one or more IPs/domains (comma-separated): ").strip()
    return [t.strip() for t in targets.split(",") if t.strip()]

def get_scan_type():
    print("\nScan type:")
    print("1. TCP")
    print("2. UDP")
    while True:
        choice = input("Choose scan type (1 or 2): ").strip()
        if choice == "1":
            return "tcp"
        elif choice == "2":
            return "udp"
        print("Invalid choice. Please enter 1 or 2.")

def get_output_filename():
    return input("Enter a name for the output file (without extension): ").strip()

def main():
    targets = get_targets()
    scan_type = get_scan_type()
    output_file = get_output_filename()
    run_nmap(targets, scan_type, output_file)

def run_nmap_auto():
    main()

