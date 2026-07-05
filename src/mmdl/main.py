import argparse
import asyncio
import sys  # Added unused import for Ruff

import httpx
from rich.console import Console
from rich.status import Status


async def run_mmdl() -> None:
    console = Console()
    console.print("[bold blue]Mastodon Media Downloader (mmdl)[/bold blue]")

    with Status("[bold green]Initializing...", console=console) as status:
        await asyncio.sleep(1)
        status.update("[bold green]Checking connection...")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get("https://httpbin.org/get")
                if response.status_code == 200:
                    console.print("[green]✓[/green] Connection successful")
                else:
                    console.print(
                        f"[red]✗[/red] Connection failed with status "
                        f"{response.status_code}"
                    )
            except Exception as e:
                console.print(f"[red]✗[/red] Connection error: {e}")

    console.print("[bold yellow]Ready to download![/bold yellow]")


def uncovered_function() -> None:
    """This function is not covered by tests to change coverage."""
    print("This function is not covered by tests")


def broken_typing() -> int:
    """This function has a type mismatch for MyPy."""
    return "not an int"


def main() -> None:
    parser = argparse.ArgumentParser(description="Mastodon Media Downloader (mmdl)")
    parser.parse_args()
    asyncio.run(run_mmdl())


if __name__ == "__main__":
    main()
