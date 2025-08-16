import logging
import click
from importlib.metadata import version, PackageNotFoundError

# Package metadata
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

# Import your tool modules
from sh00k3ms_toolkit import (
    domain_recon,
    deserialization_checker,
    endpoint_recon,
    jwt_cracker,
)

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "-v", "--verbose",
    count=True,
    help="-v for INFO, -vv for DEBUG (default WARN)"
)
@click.version_option(__version__, prog_name="sh00k3ms")
@click.pass_context
def cli(ctx: click.Context, verbose: int) -> None:
    """sh00k3ms toolkit – recon & testing helpers"""
    # default WARNING; -v -> INFO; -vv+ -> DEBUG
    level = logging.WARNING if verbose == 0 else (logging.INFO if verbose == 1 else logging.DEBUG)
    setup_logging(level)
    ctx.ensure_object(dict)
    ctx.obj["log_level"] = level

@cli.command()
@click.argument("domain")
@click.pass_context
def recon(ctx: click.Context, domain: str) -> None:
    """Run domain recon on DOMAIN"""
    log = logging.getLogger("sh00k3ms.recon")
    log.info("Running domain recon on %s", domain)
    try:
        domain_recon.run_domain_recon(domain)
    except Exception:
        log.exception("Recon failed")

@cli.command("deser")
@click.argument("target")
@click.pass_context
def deser(ctx: click.Context, target: str) -> None:
    """Check for deserialization issues on TARGET"""
    log = logging.getLogger("sh00k3ms.deser")
    log.info("Running deserialization checker on %s", target)
    try:
        deserialization_checker.run_deserialization_checker(target)
    except Exception:
        log.exception("Deserialization check failed")

@cli.command("endpoint")
@click.argument("url")
@click.pass_context
def endpoint(ctx: click.Context, url: str) -> None:
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
@click.pass_context
def jwt_crack(ctx: click.Context, token: str) -> None:
    """Crack a JWT TOKEN"""
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
