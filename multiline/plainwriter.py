from .writer import *
from . import xterm
import timeit


class PlainStream(Stream):
    def __init__(self, id, stream):
        self.id = id
        self._title = None
        self.start = timeit.default_timer()
        self.end = 0
        self.stream = stream

    def title(self, text: str):
        self._title = strip_string(text)
        print(f"{self.id} {self._title}{xterm.style.reset}", file=self.stream)

    def write(self, text: str):
        if self._title is None:
            self.title(text)
        else:
            text = strip_string(text)
            print(f"{self.id} => {text}{xterm.style.reset}", file=self.stream)

    def close(self, title: str = ''):
        self.end = timeit.default_timer()
        text = strip_string(title) if title else self._title
        time = self.end - self.start
        print(f"{self.id} {text}{xterm.style.reset} {time:6.1f}s", file=self.stream)


class PlainWriter(Writer):
    def __init__(self, stream):
        self.stream = stream
        self.inputs = {}

    def status(self, text: str):
        print(f"Status: {text}{xterm.style.reset}", file=self.stream)

    def __getitem__(self, item: str):
        if item not in self.inputs:
            self.inputs[item] = PlainStream(item, self.stream)
        return self.inputs[item]
