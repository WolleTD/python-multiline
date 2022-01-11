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
