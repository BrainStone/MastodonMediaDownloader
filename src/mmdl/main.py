import asyncio
import itertools
import random
import time
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor

import click
from rich.console import Console
from rich.live import Live
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
)
from rich.table import Column

from .progress import (
    DownloadColumnCustom,
    MofNCompleteColumnCustom,
    PercentageColumnCustom,
    TimeRemainingColumnCustom,
    TransferSpeedColumnCustom,
)

FAKE_PROFILES = ["@alice@example.com", "@bob@mastodon.social", "@charlie@tech.lgbt"]


async def discover_profile(
    profile: str, progress: Progress, task_id: TaskID
) -> list[tuple[str, int]]:
    """Simulate profile discovery and finding media links."""
    num_links = random.randint(5, 15)
    # Generate (link, size_in_bytes)
    links = [
        (
            f"https://example.com/media/{profile}/{i}.jpg",
            random.randint(1_000_000, 10_000_000),
        )
        for i in range(num_links)
    ]

    # Update total and reset progress for the profile task
    progress.update(task_id, completed=0, total=num_links)

    # Each discovery takes some time and updates the "current account" bar.
    for _ in range(num_links):
        await asyncio.sleep(random.uniform(0.1, 0.3))
        progress.advance(task_id)

    return links


def download_file(
    link: str,
    size: int,
    progress: Progress,
    task_id: TaskID,
    counter: Iterator[int],
) -> None:
    """Simulate downloading a file in chunks for better speed calculation."""
    num_chunks = 10
    chunk_size = size // num_chunks
    for i in range(num_chunks):
        time.sleep(random.uniform(0.1, 0.3))
        if i == num_chunks - 1:
            # Last chunk: handle remainder
            progress.advance(task_id, advance=size - (chunk_size * (num_chunks - 1)))
        else:
            progress.advance(task_id, advance=chunk_size)
    progress.update(task_id, completed_files=next(counter))


async def run_mmdl() -> None:
    console = Console()
    console.print("[bold blue]Mastodon Media Downloader (mmdl)[/bold blue]")

    progress = Progress(
        SpinnerColumn(finished_text="[green]✓[/green]"),
        TextColumn(
            "[progress.description]{task.description}",
            table_column=Column(width=20, no_wrap=True),
        ),
        BarColumn(bar_width=None),
        MofNCompleteColumnCustom(
            table_column=Column(width=15, no_wrap=True, justify="right")
        ),
        PercentageColumnCustom(table_column=Column(width=5, justify="right")),
        DownloadColumnCustom(table_column=Column(width=15, justify="right")),
        TransferSpeedColumnCustom(table_column=Column(width=15, justify="right")),
        TimeRemainingColumnCustom(table_column=Column(width=10, justify="right")),
        console=console,
        expand=True,
    )

    with Live(progress, console=console):
        profile_tasks = {
            profile: progress.add_task(profile, total=None, unit="posts", visible=False)
            for profile in FAKE_PROFILES
        }
        accounts_task = progress.add_task(
            "[green]Profiles", total=len(FAKE_PROFILES), unit="profiles"
        )
        overall_task = progress.add_task(
            "[magenta]Download",
            total=None,
            type="download",
            completed_files=0,
            total_files=0,
        )

        total_size = 0
        total_files = 0
        completed_files_counter = itertools.count(1)
        download_futures = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            # Profile discovery runs sequentially
            for profile in FAKE_PROFILES:
                p_task = profile_tasks[profile]
                progress.update(p_task, visible=True)
                links = await discover_profile(profile, progress, p_task)

                # Start downloading discovered links immediately
                for link, size in links:
                    total_size += size
                    total_files += 1
                    progress.update(overall_task, total_files=total_files)
                    future = executor.submit(
                        download_file,
                        link,
                        size,
                        progress,
                        overall_task,
                        completed_files_counter,
                    )
                    download_futures.append(future)

                progress.advance(accounts_task)

            # Discovery finished for all profiles, now we know the total size for
            # downloads.
            progress.update(overall_task, total=total_size)

            # Wait for all downloads to finish in the thread pool
            while any(not f.done() for f in download_futures):
                await asyncio.sleep(0.1)

    console.print("[bold yellow]✓ All downloads complete![/bold yellow]")


@click.command()
def main() -> None:
    """Mastodon Media Downloader (mmdl)"""
    asyncio.run(run_mmdl())


if __name__ == "__main__":
    main()
