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
from aws_priv_esc_analyzer import run_aws_priv_esc_analyzer
from cloud_exfil_tester import run_cloud_exfil_tester
from azure_security_tools import run_azure_security_tools
from k8s_supply_chain_checker import run_k8s_supply_chain_checker
from payload_server import run_payload_server
from loot_indexer import run_loot_indexer
from report_assist import run_report_assist
from exploit_chain_runner import run_exploit_chain_runner
from api_fuzzer import run_api_fuzzer
from waf_fuzzer import run_waf_fuzzer
from ics_scanner import run_ics_scanner
from iot_scanner import run_iot_scanner
from sip_scanner import run_sip_scanner
from lateral_movement import run_lateral_movement
from red_team_tools import run_red_team_tools
from social_engineer import run_social_engineer

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
    print("P. AWS Privilege Escalation Analyzer")
    print("Z. Cloud Exfil Tester")
    print("M. Azure Security Tools")
    print("K. K8s / Supply Chain Scanner")
    print("Y. Payload Server")
    print("L. Loot Indexer")
    print("V. Report Assist (CVSS / CWE / STRIDE)")
    print("N. Exploit Chain Runner")
    print("F. API Fuzzer")
    print("W. WAF Fuzzer")
    print("D. ICS/SCADA Scanner")
    print("O. IoT Device Scanner")
    print("Q. SIP Scanner")
    print("B. Lateral Movement Scanner")
    print("G. Red Team Support Suite")
    print("SE. Social Engineering Module")
    
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
        elif choice.upper() == "P":
            run_aws_priv_esc_analyzer()
        elif choice.upper() == "Z":
            run_cloud_exfil_tester()
        elif choice.upper() == "M":
            run_azure_security_tools()
        elif choice.upper() == "K":
            run_k8s_supply_chain_checker()
        elif choice.upper() == "Y":
            run_payload_server()
        elif choice.upper() == "L":
            run_loot_indexer()
        elif choice.upper() == "V":
            run_report_assist()
        elif choice.upper() == "N":
            run_exploit_chain_runner()
        elif choice.upper() == "F":
            run_api_fuzzer()
        elif choice.upper() == "W":
            run_waf_fuzzer()
        elif choice.upper() == "D":
            run_ics_scanner()
        elif choice.upper() == "O":
            run_iot_scanner()
        elif choice.upper() == "Q":
            run_sip_scanner()
        elif choice.upper() == "B":
            run_lateral_movement()
        elif choice.upper() == "G":
            run_red_team_tools()
        elif choice.upper() == "SE":
            run_social_engineer()
        else:
            print("Invalid selection.")  

    except KeyboardInterrupt:
        print("\n[!] User terminated the toolkit session.")

if __name__ == "__main__":
    main()

