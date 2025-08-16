import logging
from importlib.metadata import version, PackageNotFoundError
import click

APP_NAME = "sh00k3ms-toolkit"
try:
    __version__ = version(APP_NAME)
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

def setup_logging(level: int) -> None:
    try:
        from rich.logging import RichHandler
        logging.basicConfig(
            level=level,
            format="%(message)s",
            handlers=[RichHandler(rich_tracebacks=True)]
        )
    except Exception:
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s"
        )

# Optional imports: keep CLI resilient if a module is missing
try:
    from sh00k3ms_toolkit import domain_recon as _domain_recon
except Exception:
    _domain_recon = None

try:
    from sh00k3ms_toolkit import subdomain_analyzer as _subdomain
except Exception:
    _subdomain = None

from sh00k3ms_toolkit import (
    deserialization_checker,
    endpoint_recon,
    jwt_cracker,
)

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-v", "--verbose", count=True, help="-v for INFO, -vv for DEBUG (default WARN)")
@click.version_option(__version__, prog_name="sh00k3ms")
@click.pass_context
def cli(ctx: click.Context, verbose: int) -> None:
    """sh00k3ms toolkit – recon & testing helpers"""
    level = logging.WARNING if verbose == 0 else (logging.INFO if verbose == 1 else logging.DEBUG)
    setup_logging(level)
    ctx.ensure_object(dict)
    ctx.obj["log_level"] = level

# Recon: prefer domain_recon.run_domain_recon, fallback to subdomain_analyzer
@cli.command()
@click.argument("domain")
def recon(domain: str) -> None:
    """Run domain recon on DOMAIN"""
    log = logging.getLogger("sh00k3ms.recon")
    log.info("Running domain recon on %s", domain)
    try:
        if _domain_recon and hasattr(_domain_recon, "run_domain_recon"):
            _domain_recon.run_domain_recon(domain)
        elif _subdomain and (hasattr(_subdomain, "run") or hasattr(_subdomain, "run_subdomain_analyzer")):
            if hasattr(_subdomain, "run"):
                _subdomain.run(domain)
            else:
                _subdomain.run_subdomain_analyzer(domain)
        else:
            raise RuntimeError("No recon module found (domain_recon or subdomain_analyzer).")
    except Exception:
        log.exception("Recon failed")

@cli.command("deser")
@click.argument("target")
def deser(target: str) -> None:
    """Check for deserialization issues on TARGET"""
    log = logging.getLogger("sh00k3ms.deser")
    log.info("Running deserialization checker on %s", target)
    try:
        deserialization_checker.run_deserialization_checker(target)
    except Exception:
        log.exception("Deserialization check failed")

@cli.command("endpoint")
@click.argument("url")
def endpoint(url: str) -> None:
    """Perform endpoint recon on URL"""
    log = logging.getLogger("sh00k3ms.endpoint")
    log.info("Running endpoint recon on %s", url)
    try:
        endpoint_recon.run_endpoint_recon(url)
    except Exception:
        log.exception("Endpoint recon failed")

@cli.group("jwt")
def jwt_group() -> None:
    """JWT cracking utilities"""
    pass

@jwt_group.command("crack")
@click.argument("token")
def jwt_crack(token: str) -> None:
    """Crack a JWT TOKEN using wordlist"""
    log = logging.getLogger("sh00k3ms.jwt")
    log.info("Running JWT cracker")
    try:
        jwt_cracker.run_jwt_cracker(token)
    except Exception:
        log.exception("JWT crack failed")

def main() -> None:
    cli()

if __name__ == "__main__":
    main()
