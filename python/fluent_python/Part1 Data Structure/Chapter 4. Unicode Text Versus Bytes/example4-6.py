"""
Dencodeing from str to bytes: success and error handeling.
"""

octets = b'Montr\xe9al'

octets.decode('cp1252')
octets.decode('iso8859_7')
octets.decode('koi8_r')

octets.decode('utf_8') # 报错，UTF-8不支持'xe9'

octets.decode('utf_8', errors='replace') # 替换成？