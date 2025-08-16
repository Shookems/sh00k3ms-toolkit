import click
from sh00k3ms_toolkit import domain_recon, deserialization_checker, endpoint_recon, jwt_cracker

@click.group()
def cli():
    """sh00k3ms toolkit – recon & testing helpers"""
    pass

@cli.command()
@click.argument("domain")
def recon(domain):
    """Run domain recon on DOMAIN"""
    click.echo(f"[+] Running domain recon on {domain}")
    try:
        domain_recon.run_domain_recon(domain)
    except Exception as e:
        click.echo(f"[!] Recon failed: {e}", err=True)

@cli.command("deser")
@click.argument("target")
def deser(target):
    """Check for deserialization issues on TARGET"""
    click.echo(f"[+] Running deserialization checker on {target}")
    try:
        deserialization_checker.run_deserialization_checker(target)
    except Exception as e:
        click.echo(f"[!] Deserialization check failed: {e}", err=True)

@cli.command("endpoint")
@click.argument("url")
def endpoint(url):
    """Perform endpoint recon on URL"""
    click.echo(f"[+] Running endpoint recon on {url}")
    try:
        endpoint_recon.run_endpoint_recon(url)
    except Exception as e:
        click.echo(f"[!] Endpoint recon failed: {e}", err=True)

@cli.group("jwt")
def jwt_group():
    """JWT cracking utilities"""
    pass

@jwt_group.command("crack")
@click.argument("token")
def jwt_crack(token):
    """Crack a JWT token"""
    click.echo("[+] Running JWT cracker")
    try:
        jwt_cracker.run_jwt_cracker(token)
    except Exception as e:
        click.echo(f"[!] JWT crack failed: {e}", err=True)

def main():
    cli()

if __name__ == "__main__":
    main()
