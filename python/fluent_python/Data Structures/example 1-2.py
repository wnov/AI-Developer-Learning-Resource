"""
vector2d.py: a simplistic class demonstrating some special methods

It  is simplistic for didactic reasons. It lacks proper error handling, espacially in the ```__add__``` and ```__mul``` methods.

This exapmle is greatly expanded later in book.

Addition::

    >>> v1 = Vector(2, 4)
    >>> v2 = Vector(2, 1)
    >>> v1 + v2
    Vector(4, 5)

Absolute value::

    >>> v  = Vector(3, 4)
    >>> abs(v)
    5.0

Scalar multiplication::
    >>> v*3
    Vector(9, 12)
    >>> abs(v * 3)
    15.0
"""

import math

class Vector:
    def __init__(self, x = 0, y = 0) -> None:
        self.x = x
        self.y = y
    
    # 打印结果
    def __repr__(self) -> str: 
        return f'Vector({self.x!r}, {self.y!r})'
    # abs函数的行为
    def __abs__(self):
        return math.hypot(self.x, self.y)
    # bool函数的行为
    def __bool__(self):
        return bool(abs(self))
    # +算子的行为
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    # *算子的行为，只能处理v * 3而不能处理3 * v，后者需要__rmul__
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)



v1 = Vector(2, 4)
v2 = Vector(2, 1)
print(v1 + v2)

v  = Vector(3, 4)
print(abs(v))

print(v*3)
print(abs(v * 3))

