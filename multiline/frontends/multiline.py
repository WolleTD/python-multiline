from .. import xterm
import shutil
import timeit


class MultiLinePrinter:
    def __init__(self, stream):
        self.stream = stream
        dims = shutil.get_terminal_size()
        self.width = dims.columns
        # the last line has to stay empty to avoid scrolling
        self.height = dims.lines - 1
        self.start_time = timeit.default_timer()

    def format_line(self, prefix, content, time, color=xterm.fg.reset):
        time_str = f"{time:6.1f}s" if time is not None else ""
        max_len = self.width - len(time_str) - len(prefix) - 2
        if len(content) > max_len:
            content = f"{content[:max_len - 3]}..."
        return f"{color}{prefix} {content:{max_len}} {time_str}{xterm.fg.reset}"

    def _print_line(self, buffer, now, max_rows):
        lines = 0
        time = (now - buffer.start) if buffer.end == 0 else (buffer.end - buffer.start)
        color = xterm.fg.white if buffer.end == 0 else xterm.fg.blue
        print(self.format_line(buffer.id, buffer._title, time, color), file=self.stream)
        lines = lines + 1
        if buffer.end == 0:
            for line in buffer.lines[-max_rows:]:
                print(self.format_line(f" =>", line, None), file=self.stream)
                lines = lines + 1
        return lines

    def print(self, status: str, streams: dict):
        now = timeit.default_timer()
        time = now - self.start_time
        lines = 1
        print(self.format_line("Status:", status, time), file=self.stream)
        active = sum([1 for b in streams.values() if b.end == 0 and len(b.lines) > 0])
        if active > 0:
            max_rows = min((self.height - len(streams) - 1) // active, 4)
        else:
            max_rows = 4

        for buffer in streams.values():
            lines = lines + self._print_line(buffer, now, max_rows)
        return lines
