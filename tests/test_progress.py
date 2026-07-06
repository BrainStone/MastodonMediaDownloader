from unittest.mock import MagicMock

from rich.progress import Task

from mmdl.progress import (
    DownloadColumnCustom,
    MofNCompleteColumnCustom,
    PercentageColumnCustom,
    TimeRemainingColumnCustom,
    TransferSpeedColumnCustom,
)


def test_mofn_complete_column_custom_download() -> None:
    column = MofNCompleteColumnCustom()
    task = MagicMock(spec=Task)
    task.fields = {"type": "download", "completed_files": 10, "total_files": 20}

    result = column.render(task)
    assert result.plain == "10/20 files"


def test_mofn_complete_column_custom_other() -> None:
    column = MofNCompleteColumnCustom()
    task = MagicMock(spec=Task)
    task.fields = {"unit": "posts"}
    task.completed = 5
    task.total = 10

    result = column.render(task)
    assert result.plain == "5/10 posts"


def test_mofn_complete_column_custom_no_total() -> None:
    column = MofNCompleteColumnCustom()
    task = MagicMock(spec=Task)
    task.fields = {"unit": "profiles"}
    task.completed = 2
    task.total = None

    result = column.render(task)
    assert result.plain == "2/? profiles"


def test_mofn_complete_column_custom_no_unit() -> None:
    column = MofNCompleteColumnCustom()
    task = MagicMock(spec=Task)
    task.fields = {}
    task.completed = 1
    task.total = 1

    result = column.render(task)
    assert result.plain == "1/1"


def test_percentage_column_custom_download_indeterminate() -> None:
    column = PercentageColumnCustom()
    task = MagicMock(spec=Task)
    task.total = None
    task.fields = {"type": "download"}

    result = column.render(task)
    assert result.plain == "  ?%"


def test_percentage_column_custom_other_indeterminate() -> None:
    column = PercentageColumnCustom()
    task = MagicMock(spec=Task)
    task.total = None
    task.fields = {}

    result = column.render(task)
    assert result.plain == ""


def test_percentage_column_custom_determinate() -> None:
    column = PercentageColumnCustom()
    task = MagicMock(spec=Task)
    task.total = 100
    task.percentage = 50.0

    result = column.render(task)
    assert result.plain == " 50%"


def test_download_column_custom_not_download() -> None:
    column = DownloadColumnCustom()
    task = MagicMock(spec=Task)
    task.fields = {"type": "other"}

    result = column.render(task)
    assert result.plain == ""


def test_download_column_custom_indeterminate() -> None:
    column = DownloadColumnCustom()
    task = MagicMock(spec=Task)
    task.fields = {"type": "download"}
    task.total = None
    task.completed = 1024 * 1024

    result = column.render(task)
    # 1024*1024 bytes is 1.0 MB
    assert "1.0 MB/?" in result.plain


def test_transfer_speed_column_custom_no_speed() -> None:
    column = TransferSpeedColumnCustom()
    task = MagicMock(spec=Task)
    task.speed = None

    result = column.render(task)
    assert result.plain == "?/s"


def test_transfer_speed_column_custom_zero_speed() -> None:
    column = TransferSpeedColumnCustom()
    task = MagicMock(spec=Task)
    task.speed = 0

    result = column.render(task)
    assert result.plain == "?/s"


def test_transfer_speed_column_custom_other_unit() -> None:
    column = TransferSpeedColumnCustom()
    task = MagicMock(spec=Task)
    task.speed = 1.5
    task.fields = {"unit": "posts"}

    result = column.render(task)
    assert result.plain == "1.5 posts/s"


def test_transfer_speed_column_custom_long_unit() -> None:
    column = TransferSpeedColumnCustom()
    task = MagicMock(spec=Task)
    task.speed = 2.0
    task.fields = {"unit": "profiles"}

    result = column.render(task)
    assert result.plain == "2.0 prof./s"


def test_time_remaining_column_custom_none() -> None:
    column = TimeRemainingColumnCustom()
    task = MagicMock(spec=Task)
    task.time_remaining = None

    result = column.render(task)
    assert result.plain == "?:??:??"


def test_download_column_custom_determinate() -> None:
    column = DownloadColumnCustom()
    task = MagicMock()
    task.fields = {"type": "download"}
    task.total = 2000000
    task.completed = 1000000

    result = column.render(task)
    # rich's DownloadColumn uses decimal by default
    assert "1.0/2.0 MB" in result.plain


def test_transfer_speed_column_custom_download() -> None:
    column = TransferSpeedColumnCustom()
    task = MagicMock()
    task.speed = 1000000
    task.fields = {"type": "download"}
    task.finished = False
    task.finished_speed = None

    result = column.render(task)
    assert "1.0 MB/s" in result.plain


def test_time_remaining_column_custom_determinate() -> None:
    column = TimeRemainingColumnCustom()
    task = MagicMock()
    task.time_remaining = 3661  # 1h 1m 1s
    task.total = 100  # Needed by rich's TimeRemainingColumn

    result = column.render(task)
    assert "1:01:01" in result.plain
