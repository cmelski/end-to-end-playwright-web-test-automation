# run_tests.py
import sys
import subprocess
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)


def run_pytest(additional_args=None):
    """Run pytest with HTML & XML reports"""
    cmd = [
        "pytest",
        "--maxfail=5",
        "--disable-warnings",
        f"--html={REPORTS_DIR / 'report.html'}",
        f"--self-contained-html",
        f"--junitxml={REPORTS_DIR / 'results.xml'}"
    ]
    if additional_args:
        cmd += additional_args
    console.print(f"[bold cyan]Running pytest with command:[/bold cyan] {' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Display basic console summary
    console.print("[bold green]Pytest Output:[/bold green]\n")
    console.print(result.stdout)
    if result.stderr:
        console.print("[bold red]Errors:[/bold red]\n")
        console.print(result.stderr)

    # Optional: parse output for a simple summary table
    summary = [line for line in result.stdout.splitlines() if "==" in line and "in" in line]
    if summary:
        table = Table(title="Test Run Summary", box=box.ROUNDED, style="cyan")
        table.add_column("Summary")
        for s in summary:
            table.add_row(s)
        console.print(table)

    return result.returncode


def list_tests():
    """List all available tests"""
    result = subprocess.run(["pytest", "--collect-only"], capture_output=True, text=True)
    tests = [line.strip() for line in result.stdout.splitlines() if line.strip().startswith("<Function ")]
    table = Table(title="Discovered Tests", box=box.SIMPLE)
    table.add_column("Test Functions", style="magenta")
    for t in tests:
        table.add_row(t.replace("<Function ", "").replace(">", ""))
    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Smart CLI Test Runner")
    parser.add_argument("--list", action="store_true", help="List all tests")
    parser.add_argument("--rerun-failed", action="store_true", help="Rerun only failed tests")

    # parse_known_args captures known args, unknown goes to pytest
    args, unknown = parser.parse_known_args()

    if args.list:
        list_tests()
        sys.exit(0)

    # unknown contains all pytest-specific arguments like -m, -k
    additional = unknown

    if args.rerun_failed:
        # Requires pytest-rerunfailures plugin
        additional += ["--reruns", "2", "--reruns-delay", "1"]

    return_code = run_pytest(additional)

    console.print(f"\n[bold yellow]Reports generated in:[/bold yellow] {REPORTS_DIR.resolve()}")
    console.print(f"[bold yellow]HTML report:[/bold yellow] {REPORTS_DIR / 'report.html'}")
    console.print(f"[bold yellow]JUnit XML report:[/bold yellow] {REPORTS_DIR / 'results.xml'}\n")

    sys.exit(return_code)

if __name__ == "__main__":
    main()
