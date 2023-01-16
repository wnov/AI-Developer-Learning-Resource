"""
Encodeing to bytes: success and error handeling.
"""

city = 'São Paulo'
city.encode('utf8')

city.encode('utf16')

city.encode('iso8859_1')

city.encode('cp437') # 报错，cp437不支持ã字符

city.encode('cp437', errors='ignore')

city.encode('cp437', errors='replace')

city.encode('cp437', errors='xmlcharrefreplace') # 用XML entity替换不可识别的字符