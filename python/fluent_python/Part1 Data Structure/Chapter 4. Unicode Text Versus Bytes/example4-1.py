"""
Encoding and decoding.
"""

s = 'café'
print(s, len(s))

# é在UTF-8编码下有2个字节，所以长度+1
b = s.encode('utf8')
print(b, len(b))
print(b == bytes('café', encoding='utf8'))

print(b.decode('utf8'))