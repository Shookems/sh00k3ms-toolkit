import requests
import urllib.parse
import csv
import json
import os
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Load payloads
def load_payloads():
    with open("payloads/xss_css_reflected.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]
def parse_kv_string(data_str):
    return dict(urllib.parse.parse_qsl(data_str))

def test_reflected_xss_json(url, json_str, payloads):
    try:
        base_json = json.loads(json_str)
    except json.JSONDecodeError:
        print(f"{Fore.YELLOW}[-] Invalid JSON input.")
        return []

    results = []
    for key in base_json:
        for payload in payloads:
            new_json = base_json.copy()
            new_json[key] = payload
            try:
                res = requests.post(
                    url,
                    json=new_json,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                if payload in res.text:
                    print(f"{Fore.RED}[!] Reflected payload in JSON key '{key}': {payload}")
                    results.append({
                        "param": key,
                        "payload": payload,
                        "url": url,
                        "reflected": True,
                        "method": "POST-JSON"
                    })
                else:
                    print(f"{Fore.GREEN}[+] Safe JSON key '{key}' with payload: {payload}")
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Error on JSON POST {url}: {e}")

    return results
def test_reflected_xss_post(url, data_str, payloads):
    base_data = parse_kv_string(data_str)
    results = []

    for param in base_data:
        for payload in payloads:
            new_data = base_data.copy()
            new_data[param] = payload

            try:
                res = requests.post(url, data=new_data, timeout=10)
                if payload in res.text:
                    print(f"{Fore.RED}[!] Reflected payload in param '{param}' (POST): {payload}")
                    results.append({
                        "param": param,
                        "payload": payload,
                        "url": url,
                        "reflected": True,
                        "method": "POST"
                    })
                else:
                    print(f"{Fore.GREEN}[+] Safe param '{param}' with payload (POST): {payload}")
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Error on POST {url}: {e}")

    return results

def run_reflected_tester():
    url = input("Enter URL to test (include params for GET): ").strip()
    method = input("Use GET or POST? [GET/POST]: ").strip().upper()

    payloads = load_payloads()
    results = []

    if method == "POST":
        data_str = input("Enter POST data (e.g. username=admin&password=123): ").strip()
        results = test_reflected_xss_post(url, data_str, payloads)
    elif method == "GET":
        if "?" not in url:
            print(f"{Fore.YELLOW}[-] GET URL must include parameters.")
            return
        results = test_reflected_xss(url, payloads)
    else:
        print(f"{Fore.YELLOW}[-] Invalid method selected.")
        return

    save_results(results)

# Inject payload into each parameter and check response
def test_reflected_xss(url, payloads):
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)

    results = []
    for param in query:
        for payload in payloads:
            new_query = query.copy()
            new_query[param] = payload
            encoded_query = urllib.parse.urlencode(new_query, doseq=True)
            full_url = urllib.parse.urlunparse(
                parsed._replace(query=encoded_query)
            )

            try:
                res = requests.get(full_url, timeout=10)
                if payload in res.text:
                    print(f"{Fore.RED}[!] Reflected payload in param '{param}': {payload}")
                    results.append({
                        "param": param,
                        "payload": payload,
                        "url": full_url,
                        "reflected": True
                    })
                else:
                    print(f"{Fore.GREEN}[+] Safe param '{param}' with payload: {payload}")
            except Exception as e:
                print(f"{Fore.YELLOW}[!] Error requesting {full_url}: {e}")

    return results

# Save results to CSV
def save_results(results):
    if not results:
        return
    os.makedirs("results", exist_ok=True)
    filename = f"results/reflected_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["param", "payload", "url", "reflected", "method"])
        writer.writeheader()
        writer.writerows(results)
    print(f"\n{Fore.CYAN}[✓] Results saved to {filename}")

# Entry point for main.py
def run_reflected_tester():
    url = input("Enter URL to test (include params for GET): ").strip()
    method = input("Use GET, POST, or POST-JSON? [GET/POST/JSON]: ").strip().upper()
    
    payloads = load_payloads()
    results = []

    if method == "POST":
        data_str = input("Enter POST data (e.g. username=admin&password=123): ").strip()
        results = test_reflected_xss_post(url, data_str, payloads)
    elif method == "JSON":
        json_str = input("Enter raw JSON body (e.g. {\"search\": \"test\"}): ").strip()
        results = test_reflected_xss_json(url, json_str, payloads)
    elif method == "GET":
        if "?" not in url:
            print(f"{Fore.YELLOW}[-] GET URL must include parameters.")
            return
        results = test_reflected_xss(url, payloads)
    else:
        print(f"{Fore.YELLOW}[-] Invalid method selected.")
        return

    save_results(results)

