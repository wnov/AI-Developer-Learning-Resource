"""
Parameterized decorators allow people to customize decorator behavior according to parameters.
If we want to achieve different method through one single decorator, we will need parameterziation.
"""

import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(fmt=DEFAULT_FMT):

    def decorate(func):

        def clocked(*_args):
            t0 = time.perf_counter()
            _result = func(*_args)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result

        return clocked

    return decorate


@clock()
def snooze(seconds):
    time.sleep(seconds)


@clock('{name}: {elapsed}s')
def snooze_1(seconds):
    time.sleep(seconds)


if __name__ == '__main__':
    for i in range(3):
        snooze(.123)
        snooze_1(.123)