import asyncio
import shutil
import timeit
from . import xterm
from .writer import *
from .frontends import MultiLinePrinter


class TtyStream(Stream):
    def __init__(self, stream_id: str):
        self.id = stream_id
        self._title = None
        self.start = timeit.default_timer()
        self.end = 0
        self.lines = []

    def title(self, text: str):
        self._title = strip_string(text)

    def write(self, text: str):
        if self._title is None:
            self.title(text)
        else:
            self.lines.append(strip_string(text))

    def close(self, title: str = ''):
        if title:
            self._title = title
        self.end = timeit.default_timer()


class TtyWriter(Writer):
    def __init__(self, stream, frontend=MultiLinePrinter):
        self.stream = stream
        self.printer = frontend(stream)
        dims = shutil.get_terminal_size()
        self.width = dims.columns
        # the last line has to stay empty to avoid scrolling
        self.height = dims.lines - 1
        self.status_text = "Multiline startup"
        self.refresh_rate = 0.01
        self.running = False
        self.task = None
        self.inputs = {}

    def start(self):
        self.running = True
        self.task = asyncio.create_task(self.run())

    async def stop(self):
        self.running = False
        await self.task

    def status(self, text: str):
        self.status_text = text

    def __getitem__(self, item: str):
        if item not in self.inputs:
            self.inputs[item] = TtyStream(item)
        return self.inputs[item]

    async def run(self):
        print(xterm.civis, end='', file=self.stream)

        try:
            while True:
                lines = self.printer.print(self.status_text, self.inputs)

                if not self.running:
                    break
                await asyncio.sleep(self.refresh_rate)
                print(xterm.ed + xterm.cuu(lines), end='', file=self.stream)
        finally:
            print(xterm.cnorm, end='', file=self.stream)
