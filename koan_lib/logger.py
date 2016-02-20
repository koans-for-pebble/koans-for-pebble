from __future__ import print_function

_logging_verbosity = 0


class Logger:
    colors = {
        'dbg': '\033[95m',
        'warn': '\033[93m\033[1m',
        'err': '\033[91m\033[1m',
        'fail': '\033[41m\033[30m\033[1m',
        'pass': '\033[42m\033[30m\033[1m',
        'win': '\033[44m\033[30m\033[1m',
        'wisdom': '\033[96m\033[1m',
        'experience': '\033[32m\033[1m',
        'info': '(i) ',
        'normal': '\033[0m'
    }

    def __init__(self, verbosity=None):
        if verbosity is not None:
            print("Setting verbosity to", verbosity)
            global _logging_verbosity
            _logging_verbosity = verbosity

    def log(self, importance, text):
        global _logging_verbosity
        if importance == 'dbg' and _logging_verbosity < 1:
            return  # Don't print debug logs if the code verbosity is low.
        if importance not in self.colors.keys():
            # If the color doesn't exist
            print('error: bad importance %s' % [importance])
        try:
            # Try to write the selected color
            print(self.colors[importance], end='')
        except KeyError as e:
            # If the color doesn't exist, write the error.
            print(e)
        if text.__class__ is tuple:
            # If the text is a tuple:
            print(' '.join([str(x) for x in text])
                  .replace('\\n', '\n'), end='')
        else:
            # If the text isn't a tuple, just write it.
            print(text, end="")
        print(self.colors['normal'])

    def line(self):
        # Print a newline.
        print()
