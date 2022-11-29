"""
A deck as a sequence of playing cards
"""

import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self) -> None:
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]


beer_card = Card('7', 'diamonds')
print(beer_card)
# __len__方法指导len()函数的结果
deck = FrenchDeck()
print(len(deck))
# __getitem__方法指导[]操作的结果
print(deck[0])
print(deck[-1])


from random import choice

print(choice(deck))

print(deck[:3])
print(deck[12::13])
# 像遍历数组一样遍历deck对象
for card in deck:
    print(card)

for car in reversed(deck):
    print(card)

# in 关键字在对象没有__contains__方法时会做一次序列遍历
print(Card('Q', 'hearts') in deck)
print(Card('7', 'beasts') in deck)


suit_values = dict(spades = 3, hearts = 2, diamonds = 1, clubs = 0)

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in sorted(deck, key=spades_high):
    print(card)

# FrenchDeck类隐式继承object类，但是有很多方法都没有实现。不过在实现__len__和__getitem__方法后，FrenchDeck的功能和标准的python序列
# 类似了，我们可以使用迭代和切片的方法来获取元素。不过当前元素还不能实现shuffle功能，因为FrenchDeck是不可变对象，13章介绍__setitem__方法
# 后可以解决这个问题。

