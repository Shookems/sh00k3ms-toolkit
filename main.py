from rich.console import Console
from rich.table import Table
import subprocess
import sys

console = Console()

tools = {
    "1": {
        "name": "Domain Recon (WHOIS + DNS)",
        "command": "python domain_recon.py"
    },
    "2": {
        "name": "Cron Job Generator",
        "command": "python cron_gen.py"
    },
    "3": {
        "name": "Endpoint Vulnerability Scanner",
        "command": "python endpoint_recon.py"
    }
}

def show_menu():
    table = Table(title="sh00k3ms-toolkit", show_lines=True)
    table.add_column("Option", justify="center", style="cyan")
    table.add_column("Tool", style="green")

    for key, tool in tools.items():
        table.add_row(key, tool["name"])
    table.add_row("0", "[red]Exit[/red]")

    console.print(table)

def main():
    show_menu()
    choice = input("Select a tool to run: ").strip()

    if choice == "0":
        console.print("Exiting. Have a great day! 👋", style="bold red")
        sys.exit(0)
    elif choice in tools:
        tool = tools[choice]
        if "domain_recon" in tool["command"]:
            domain = input("Enter a domain name (e.g., openai.com): ").strip()
            output = input("Optional: enter CSV filename or leave blank: ").strip()
            full_cmd = f"{tool['command']} {domain}"
            if output:
                full_cmd += f" -o {output}"
        else:
            full_cmd = tool["command"]

        console.print(f"Running: [bold yellow]{full_cmd}[/bold yellow]")
        subprocess.run(full_cmd, shell=True)
    else:
        console.print("Invalid option. Please try again.", style="bold red")

if __name__ == "__main__":
    main()
