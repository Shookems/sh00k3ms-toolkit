from modules.reflected_tester import run_reflected_tester
from endpoint_recon import run_endpoint_recon
from cron_gen import run_cron_gen
from domain_recon import run_domain_recon
from nmap_auto import run_nmap_scanner
from tls_checker import run_tls_checker
from xss_css_checker import run_xss_css_checker

def main():
    print("=== Sh00k3ms Toolkit ===")
    print("1. Reflected XSS / CSS Injection Tester")
    print("2. Endpoint Recon Tool")
    print("3. Cron Job Generator")
    print("4. Domain Recon Tool")
    print("5. Nmap Auto Scanner")
    print("6. TLS Checker")
    print("X. Run XSS & CSS Injection Checker")
    
    choice = input("Select a tool: ")

    if choice == "1":
        run_reflected_tester()
    elif choice == "2":
        run_endpoint_recon()
    elif choice == "3":
        run_cron_gen()
    elif choice == "4":
        run_domain_recon()
    elif choice == "5":
        run_nmap_scanner()
    elif choice == "6":
        run_tls_checker()
    elif choice.upper() == "X":
        run_xss_css_checker()
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()

