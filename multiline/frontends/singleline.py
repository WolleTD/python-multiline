from .. import xterm
from ..writer import strip_string
import shutil
import timeit


class SingleLinePrinter:
    def __init__(self, stream):
        self.stream = stream
        dims = shutil.get_terminal_size()
        self.width = dims.columns
        # the last line has to stay empty to avoid scrolling
        self.height = dims.lines - 1
        self.start_time = timeit.default_timer()

    def format_line(self, prefix, content, time, color=xterm.fg.reset):
        time_str = f"{time:6.1f}s" if time is not None else ""
        max_len = self.width - len(time_str) - len(strip_string(prefix)) - 2
        if len(content) > max_len:
            content = f"{content[:max_len - 3]}..."
        return f"{prefix} {color}{content:{max_len}}{xterm.fg.reset} {time_str}"

    def _print_line(self, buffer, now):
        time = (now - buffer.start) if buffer.end == 0 else (buffer.end - buffer.start)
        if len(buffer.lines) > 0 and buffer.end == 0:
            line = buffer.lines[-1]
            color = xterm.fg.reset
        else:
            line = buffer._title
            color = xterm.fg.reset if buffer.end == 0 else xterm.fg.white
        print(self.format_line(buffer.id, line, time, color), file=self.stream)
        return 1

    def print(self, status, streams):
        now = timeit.default_timer()
        time = now - self.start_time
        lines = 1
        print(self.format_line("Status:", status, time), file=self.stream)

        for buffer in streams.values():
            lines = lines + self._print_line(buffer, now)
        return lines


