import re


class Stream:
    def title(self, text: str):
        pass

    def write(self, text: str):
        pass

    def close(self, title: str = ''):
        pass


class Writer:
    def start(self):
        pass

    async def stop(self):
        pass

    def status(self, text: str):
        pass

    def __getitem__(self, item: str) -> Stream:
        pass


_strip_escape = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")


def strip_string(string):
    # Remove all \r and take the last part, remove all \n and take the first part,
    # remove all escape sequences
    return _strip_escape.sub('', string.rsplit('\r', 1)[0].split('\n', 1)[0])
