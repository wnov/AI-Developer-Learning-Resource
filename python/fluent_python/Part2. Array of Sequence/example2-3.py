"""
Build a list by a listcomp and a map/filter composition
"""

symbols = "$¢£¥€¤"
beyond_ascii = [ord(symbol) for symbol in symbols if ord(symbol) > 127]
print(beyond_ascii)

beyond_ascii = list(filter(lambda x : x > 127, map(ord, symbols)))
print(beyond_ascii)
