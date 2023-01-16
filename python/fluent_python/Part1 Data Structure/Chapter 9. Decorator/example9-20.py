"""
Implementation of function singledispatch to deal with different data type with
only one function api.
"""

from functools import singledispatch
from collections import abc
import fractions
import decimal
import html
import numbers


# 这个函数是默认操作，下面其他实现是具体类型的操作方法
@singledispatch
def htmlize(obj: object) -> str:
    content = html.escape(repr(obj))
    return f'<pre>{content}</pre>'


@htmlize.register
def _(text: str):
    content = html.escape(repr(text)).replace('\n', '<br/>\n')
    return f'<pre>{content}</pre>'


@htmlize.register
def _(seq: abc.Sequence) -> str:
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'


@htmlize.register
def _(n: numbers.Integral) -> str:
    return f'<pre>{n} (0x{n:x})</pre>'


@htmlize.register
def _(n: bool) -> str:
    return f'<pre>{n}</pre>'


@htmlize.register(fractions.Fraction)
def _(x) -> str:
    frac = fractions.Fraction(x)
    return f'<pre>{frac.numerator}/{frac.denominator}</pre>'


@htmlize.register(decimal.Decimal)
@htmlize.register(float)
def _(x) -> str:
    frac = fractions.Fraction(x).limit_denominator()
    return f'<pre>{x} ({frac.numerator}/{frac.denominator})</pre>'


if __name__ == '__main__':
    print(htmlize({1, 2, 3}))
    print(htmlize(abs))
    print('Heimlich & Co.\n- a game')
    print(htmlize(42))
