from .plainwriter import PlainWriter
from .ttywriter import TtyWriter
from .frontends import *

def create(stream, frontend=MultiLinePrinter):
    if stream.isatty():
        return TtyWriter(stream, frontend)
    else:
        return PlainWriter(stream)
