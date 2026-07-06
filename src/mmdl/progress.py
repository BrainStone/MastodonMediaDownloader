from rich.filesize import decimal
from rich.progress import (
    DownloadColumn,
    MofNCompleteColumn,
    ProgressColumn,
    Task,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.text import Text


class MofNCompleteColumnCustom(MofNCompleteColumn):
    def render(self, task: "Task") -> Text:
        if task.fields.get("type") == "download":
            completed = task.fields.get("completed_files", 0)
            total = task.fields.get("total_files", 0)
            return Text(f"{completed}/{total} files", style="progress.download")

        completed = int(task.completed)
        total = int(task.total) if task.total is not None else "?"
        unit = task.fields.get("unit", "")
        res = Text(f"{completed}/{total}", style="progress.download")
        if unit:
            res.append(f" {unit}")
        return res


class PercentageColumnCustom(ProgressColumn):
    def render(self, task: "Task") -> Text:
        if task.total is None:
            if task.fields.get("type") == "download":
                return Text("  ?%", style="progress.percentage")
            return Text("")
        return Text(f"{task.percentage:>3.0f}%", style="progress.percentage")


class DownloadColumnCustom(DownloadColumn):
    def render(self, task: "Task") -> Text:
        if task.fields.get("type") != "download":
            return Text("")
        if task.total is None:
            completed = decimal(int(task.completed))
            return Text(f"{completed}/?", style="progress.download")
        return super().render(task)


class TransferSpeedColumnCustom(TransferSpeedColumn):
    def render(self, task: "Task") -> Text:
        if task.speed is None or task.speed == 0:
            return Text("?/s", style="progress.data.speed")

        if task.fields.get("type") == "download":
            return super().render(task)
        else:
            unit = task.fields.get("unit", "it")
            # Abbreviate unit if too long
            if len(unit) > 5:
                unit = unit[:4] + "."
            return Text(f"{task.speed:.1f} {unit}/s", style="progress.data.speed")


class TimeRemainingColumnCustom(TimeRemainingColumn):
    def render(self, task: "Task") -> Text:
        if task.time_remaining is None:
            return Text("?:??:??", style="progress.remaining")
        return super().render(task)
