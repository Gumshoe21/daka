import time
from time import sleep
from rich.table import Column
from rich.progress import track, Progress, TimeElapsedColumn, TextColumn, BarColumn
from rich.text import Text
from rich.console import Console


class Timer:
    def __init__(self, name: str, mode: str, duration: int) -> None:
        self.name = name
        self.mode = mode
        self.duration = duration
        self.console = Console()


class Stopwatch(Timer):
    def __init__(self, name: str, duration: int):
        super().__init__(name=name, mode="stopwatch", duration=duration)

    def start(self):
        time_elapsed_col = TimeElapsedColumn()
        stopwatch_time = Progress(time_elapsed_col, expand=False)
        with stopwatch_time:
            for n in stopwatch_time.track(range(999999999)):
                sleep(0.1)


class Countdown(Timer):
    def __init__(self, name: str, duration: int):
        super().__init__(name=name, mode="stopwatch", duration=duration)

    def start(self):
        progress = self.duration
        for second in track(range(progress, 0, -1), description="Running timer."):
            time.sleep(0.01)
            progress -= 1
        text = Text()
        text.append("Timer finished", style="bold magenta")
        self.console.print(text)
