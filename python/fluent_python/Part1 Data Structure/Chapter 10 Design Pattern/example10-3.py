"""
Globals() usage to accompplish max discount.
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from decimal import Decimal
from typing import NamedTuple, Callable


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.quantity * self.price


class Order(NamedTuple):
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Callable[['Order'], Decimal] = None

    def total(self) -> Decimal:
        return sum(item.total() for item in self.cart)

    def due(self) -> Decimal:
        return self.total() - self.promotion(self)

    def __repr__(self) -> str:
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'


def fidelity_promo(order: Order) -> Decimal:
    rate = Decimal(0.05)
    if order.customer.fidelity >= 1000:
        return order.total() * rate
    return Decimal(0.)


def bulk_item_promo(order: Order) -> Decimal:
    discount = Decimal(0.)
    for item in order.cart:
        if item.quantity >= 20:
            discount += Decimal(0.1) * item.total()
    return discount


def large_order_promo(order: Order) -> Decimal:
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal(0.07)
    return Decimal(0.)


promos = [
    promo for name, promo in globals().items()
    if name.endswith('_promo') and name != 'best_promo'
]


def best_promo(order: Order) -> Decimal:
    return max(promo(order) for promo in promos)
