from unittest.mock import MagicMock, patch

import pytest

from mmdl.main import run_mmdl


@pytest.mark.asyncio
async def test_run_mmdl_import() -> None:
    assert run_mmdl is not None

@pytest.mark.asyncio
@patch("mmdl.main.httpx.AsyncClient")
@patch("mmdl.main.asyncio.sleep", return_value=None)
async def test_run_mmdl_execution(
    mock_sleep: MagicMock, mock_async_client: MagicMock
) -> None:
    # Mock the context manager and the get request
    mock_client = MagicMock()
    mock_async_client.return_value.__aenter__.return_value = mock_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_client.get.return_value = mock_response

    await run_mmdl()

    mock_client.get.assert_called_once_with("https://httpbin.org/get")
