from unittest.mock import ANY, MagicMock, patch

import pytest

from mmdl.main import run_mmdl


@pytest.mark.asyncio
async def test_run_mmdl_import() -> None:
    assert run_mmdl is not None


@pytest.mark.asyncio
@patch("mmdl.main.time.sleep", return_value=None)
@patch("mmdl.main.asyncio.sleep", return_value=None)
@patch("mmdl.main.Progress")
@patch("mmdl.main.Live")
async def test_run_mmdl_execution(
    mock_live_class: MagicMock,
    mock_progress_class: MagicMock,
    mock_async_sleep: MagicMock,
    mock_time_sleep: MagicMock,
) -> None:
    # Setup mock progress
    mock_progress = MagicMock()
    mock_progress_class.return_value = mock_progress

    # Mock add_task to return some task IDs
    # 3 profiles + 2 aggregate bars = 5 tasks
    mock_progress.add_task.side_effect = range(1, 6)

    await run_mmdl()

    # Verify that Live was used
    mock_live_class.assert_called_once()

    # Verify that tasks were added
    assert mock_progress.add_task.call_count == 5

    # Verify that advance and update were called
    assert mock_progress.advance.call_count > 0
    assert mock_progress.update.call_count > 0

    # Check that overall progress bar was updated to be determinate at the end
    # overall_task is the last one added (ID 5)
    mock_progress.update.assert_any_call(5, total=ANY)
