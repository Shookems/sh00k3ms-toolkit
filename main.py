from modules.reflected_tester import run_reflected_tester
from endpoint_recon import run_endpoint_recon
from cron_gen import run_cron_gen
from domain_recon import run_domain_recon
from nmap_auto import run_nmap_scanner
from tls_checker import run_tls_checker
from xss_css_checker import run_xss_css_checker
from deserialization_checker import run_deserialization_checker
from sqli_tester import run_sqli_tester
from header_analyzer import run_header_analyzer

def main():
    print("=== Sh00k3ms Toolkit ===")
    print("1. Reflected XSS / CSS Injection Tester")
    print("2. Endpoint Recon Tool")
    print("3. Cron Job Generator")
    print("4. Domain Recon Tool")
    print("5. Nmap Auto Scanner")
    print("6. TLS Checker")
    print("7. Run XSS & CSS Injection Checker")
    print("8. Deserialization Checker")
    print("9. SQL Injection Tester")
    print("10. HTTP Header Analyzer")

    try:
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
        elif choice.upper() == "7":
            run_xss_css_checker()
        elif choice.upper() == "8":
            run_deserialization_checker()
        elif choice.upper() == "9":
            run_sqli_tester()
	elif choice.upper() == "10":
	    run_header_analyzer()

        else:
            print("Invalid selection.")
    except KeyboardInterrupt:
        print("\n[!] User terminated the toolkit session.")

if __name__ == "__main__":
    main()

