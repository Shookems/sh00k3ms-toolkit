import argparse
import whois
import dns.resolver
import csv

def get_args():
    parser = argparse.ArgumentParser(description="Domain Recon Script")
    parser.add_argument("domain", help="Domain name to look up")
    parser.add_argument("-o", "--output", help="CSV output file")
    return parser.parse_args()

def run_whois(domain):
    try:
        w = whois.whois(domain)
        return {
            'domain_name': w.get('domain_name'),
            'registrar': w.get('registrar'),
            'creation_date': w.get('creation_date'),
            'expiration_date': w.get('expiration_date')
        }
    except Exception as e:
        print(f"WHOIS error: {e}")
        return {}

def resolve_dns(domain):
    results = {'a_records': [], 'ns_records': []}

    try:
        results['a_records'] = [rdata.address for rdata in dns.resolver.resolve(domain, 'A')]
    except Exception as e:
        print(f"A record error: {e}")

    try:
        results['ns_records'] = [str(rdata.target) for rdata in dns.resolver.resolve(domain, 'NS')]
    except Exception as e:
        print(f"NS record error: {e}")

    return results

def write_to_csv(domain, whois_data, dns_data, output_file):
    try:
        with open(output_file, mode='w', newline='') as csvfile:
            fieldnames = ['domain', 'registrar', 'creation_date', 'expiration_date', 'a_records', 'ns_records']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({
                'domain': domain,
                'registrar': whois_data.get('registrar'),
                'creation_date': whois_data.get('creation_date'),
                'expiration_date': whois_data.get('expiration_date'),
                'a_records': ', '.join(dns_data['a_records']),
                'ns_records': ', '.join(dns_data['ns_records'])
            })

            print(f"\nData written to {output_file}")
    except Exception as e:
        print(f"CSV write error: {e}")

def main():
    args = get_args()
    whois_data = run_whois(args.domain)
    dns_data = resolve_dns(args.domain)

    if args.output:
        write_to_csv(args.domain, whois_data, dns_data, args.output)
    else:
        print("\nWHOIS Data:", whois_data)
        print("DNS Data:", dns_data)

if __name__ == "__main__":
    main()

