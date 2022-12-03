"""
Build a list of Unicode code pints from a string.
"""

symbols = "$¢£¥€¤"
codes = []

for symbols in symbols:
    codes.append(ord(symbols))

print(codes)
