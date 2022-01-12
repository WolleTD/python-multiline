class Stream:
    def title(self, text: str):
        pass

    def write(self, text: str):
        pass

    def close(self, title: str = ''):
        pass

    def tail_dump(self, lines: int):
        pass


class Writer:
    def start(self):
        pass

    async def stop(self):
        pass

    def status(self, text: str):
        pass

    def tail_msg(self, text: str):
        pass

    def __getitem__(self, item: str) -> Stream:
        pass
