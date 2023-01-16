import time 
import functools

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        args = [repr(m) for m in args]
        args.extend(f'{k}: {v}' for k, v in kwargs.items())
        args_str = ', '.join(args)
        print(f'[{elapsed:0.8f}s] {name}({args_str}) -> {result}')

        return result
    return clocked


