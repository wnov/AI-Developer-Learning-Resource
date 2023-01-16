"""
Build a list of Unicode code pints from a string.
"""

symbols = "$¢£¥€¤"
codes = [ord(symbol) for symbol in symbols]

print(codes)
