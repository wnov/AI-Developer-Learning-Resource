"""
Memorization with functools.cache.
Compare difference between 2 application
"""

from example9_16 import clock
from functools import lru_cache


@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


@lru_cache
@clock
def fibonacci_cache(n):
    if n < 2:
        return n
    return fibonacci_cache(n - 2) + fibonacci_cache(n - 1)


if __name__ == '__main__':
    fibonacci(6)
    print("============================================")
    # 使用lru_cache后，函数执行结果被缓存到cache中，可以看到递归的重复执行消失了，整体函数执行效率提升明显
    fibonacci_cache(6)
