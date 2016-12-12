from os import environ

from clint.textui import puts, puts_err, colored


class Logger:
    def __init__(self, lazy_server):
        self.LOG_LEVEL = environ.get('LOG_LEVEL', 'INFO')
        self.lazy_server = lazy_server

    def puts(self, message, color=None):
        if color:
            puts(color(message))
        else:
            puts(message)

    def info(self, message):
        self.puts(message, colored.cyan)

    def debug(self, message):
        self.puts(message, colored.white)

    def warning(self, message):
        self.puts(message, colored.yellow)

    def success(self, message):
        self.puts(message, colored.green)

    def error(self, message):
        puts_err(message)
