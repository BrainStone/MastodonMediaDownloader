import asyncio

import click
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


@click.command()
def main() -> None:
    """Mastodon Media Downloader (mmdl)"""
    asyncio.run(run_mmdl())


if __name__ == "__main__":
    main()
