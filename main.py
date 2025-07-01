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
from csp_analyzer import run_csp_analyzer
from open_redirect_checker import run_open_redirect_checker
from jwt_cracker import run_jwt_cracker
from subdomain_analyzer import run_subdomain_analyzer
from cdn_edge_mapper import run_cdn_edge_mapper
from tabnabbing_checker import run_tabnabbing_checker
from iframe_worker_checker import run_iframe_worker_checker
from storage_service_checker import run_storage_service_checker
from js_injector import run_js_injector
from aws_cred_theft_detector import run_aws_cred_theft_detector

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
    print("H. HTTP Header Analyzer")
    print("C. CSP Analyzer")
    print("R. Open Redirect Checker")
    print("J. JWT Cracker")
    print("U. Subdomain Analyzer")
    print("E. CDN Edge Mapper")
    print("T. Tabnabbing Checker")
    print("I. Iframe & WebWorker Detector")
    print("S. Storage & ServiceWorker Scanner")
    print("X. JS Injector")
    print("A. AWS Credential Theft Detector")
    
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
        elif choice == "7":
            run_xss_css_checker()
        elif choice == "8":
            run_deserialization_checker()
        elif choice == "9":
            run_sqli_tester()
        elif choice.upper() == "H":
            run_header_analyzer()
        elif choice.upper() == "C":
            run_csp_analyzer()
        elif choice.upper() == "R":
            run_open_redirect_checker()
        elif choice.upper() == "J":
            run_jwt_cracker()
        elif choice.upper() == "U":
            run_subdomain_analyzer()
        elif choice.upper() == "E":
            run_cdn_edge_mapper()
        elif choice.upper() == "T":
            run_tabnabbing_checker()
        elif choice.upper() == "I":
            run_iframe_worker_checker()
        elif choice.upper() == "S":
            run_storage_service_checker()
        elif choice.upper() == "X":
            run_js_injector()
        elif choice.upper() == "A":
            run_aws_cred_theft_detector()
        else:
            print("Invalid selection.")  

    except KeyboardInterrupt:
        print("\n[!] User terminated the toolkit session.")

if __name__ == "__main__":
    main()

