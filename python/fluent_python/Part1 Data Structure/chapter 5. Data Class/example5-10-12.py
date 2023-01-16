"""
Testing type hints in different ways.
"""

class DemoPlainClass:
    a: int
    b: float = 1.1
    c = 'spam'

import typing

"""
继承NamedTuple后可以直接访问a
"""
class DemoNTClass(typing.NamedTuple):
    a: int
    b: float = 1.1
    c = 'spam'

from dataclasses import dataclass, field

@dataclass
class DemoDataClass:
    a: int
    b: float = 1.1
    c = 'spam'

@dataclass(frozen=True)
class DemoFrozenClass:
    a: int
    b: float = 1.1
    c = 'spam'


# 不能直接访问a
print(DemoPlainClass.__annotations__, DemoPlainClass.b, DemoPlainClass.c)
# 可以直接访问a
print(DemoNTClass.__doc__, DemoNTClass.a, DemoNTClass.b, DemoNTClass.c, DemoNTClass(3).a)
# 实例化之后可以访问a
print(DemoDataClass.b, DemoDataClass.c, DemoDataClass(3).a)
# frozen只有依旧不能访问
# print(DemoFrozenClass.a)