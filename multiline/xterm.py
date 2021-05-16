
civis = '\x1b[?25l'
cnorm = '\x1b[34h\x1b[?25h'

ed = '\x1b[J'
_cuu = '\x1b[{}A'


def cuu(count):
    return _cuu.format(count)


class fg:
    black   = '\033[30m'
    red     = '\033[31m'
    green   = '\033[32m'
    yellow  = '\033[33m'
    blue    = '\033[34m'
    magenta = '\033[35m'
    cyan    = '\033[36m'
    white   = '\033[37m'
    reset   = '\033[39m'


class bg:
    black   = '\033[40m'
    red     = '\033[41m'
    green   = '\033[42m'
    yellow  = '\033[43m'
    blue    = '\033[44m'
    magenta = '\033[45m'
    cyan    = '\033[46m'
    white   = '\033[47m'
    reset   = '\033[49m'


class style:
    bright = '\033[1m'
    dim    = '\033[2m'
    normal = '\033[22m'
    reset  = '\033[0m'
