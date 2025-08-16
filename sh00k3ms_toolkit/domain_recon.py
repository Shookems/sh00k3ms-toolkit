from __future__ import annotations
import dns.resolver

def run_domain_recon(domain: str) -> None:
    """
    Minimal DNS recon (A, MX, NS). Expand as you like.
    """
    lookups = [("A", "A records"), ("MX", "MX records"), ("NS", "NS records")]
    for qtype, label in lookups:
        print(f"\n=== {label} for {domain} ===")
        try:
            for r in dns.resolver.resolve(domain, qtype):
                print(str(r))
        except Exception as e:
            print(f"(no {qtype} / error: {e})")
