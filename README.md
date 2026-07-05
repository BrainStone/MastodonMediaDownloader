# Mastodon Media Downloader (mmdl)

Tool to download all media objects from any Mastodon server.

## Overview

`mmdl` is a modern CLI tool built with Python 3.12+, utilizing `asyncio` for high-performance downloads and `rich` for a beautiful terminal interface.

## Prerequisites

- **Python 3.12+** (Managed via `pyenv` recommended)
- **uv**: Lightning-fast Python package manager. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd MastodonMediaDownloader
   ```

2. Install dependencies and set up the environment:
   ```bash
   uv sync --no-dev
   ```

3. (Optional) Install as a standalone CLI command:
   ```bash
   uv tool install .
   ```

## Usage

### Using uv (Recommended for Development)

Run the tool without installing it globally:

```bash
uv run mmdl
```

### As a Standalone Command

If you performed the optional installation step, you can run it directly:

```bash
mmdl
```

For help and available options:

```bash
mmdl --help
```

## Development

### Environment Setup

Ensure your development environment is up to date:

```bash
uv sync
```

### Running Tests

Execute the test suite using `pytest`:

```bash
uv run pytest
```

### Linting and Type Checking

We use `ruff` for linting and `mypy` for static type checking.

- **Ruff (Linting & Formatting):**
  ```bash
  uv run ruff check .
  ```
- **Mypy (Type Checking):**
  ```bash
  uv run mypy .
  ```

### CI/CD

This project uses GitLab CI for automated testing and linting. Refer to `.gitlab-ci.yml` for the pipeline configuration.

## Project Structure

- `src/mmdl/`: Main source code.
- `tests/`: Unit and integration tests.
- `pyproject.toml`: Project configuration and dependencies.
