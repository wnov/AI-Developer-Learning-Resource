import math
from array import array
from math import hypot
from typing import Tuple


class Vector2d:
    typecode = 'd'

    def __init__(self, x, y) -> None:
        self.x = float(x)
        self.y = float(y)

    def __iter__(self) -> Tuple[float]:
        return (it for it in (self.x, self.y))

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f'{class_name}({self.x}, {self.y})'

    def __bytes__(self):
        return (bytes(ord(self.typecode)) + bytes(array(self.typecode, self)))

    def __eq__(self, vObject):
        return tuple(self) == tuple(vObject)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return self.x == 0 and self.y == 0

    def __format__(self, format_desc):
        if format_desc.endswith('p'):
            format_desc = format_desc[:-1]
            coords = (abs(self), math.atan2(self.y, self.x))
            out_format = '<{}, {}>'
        else:
            coords = self
            out_format = '({}, {})'
        components = (format(c, format_desc) for c in coords)
        return out_format.format(*components)
