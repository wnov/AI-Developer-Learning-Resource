"""
Encoding and decoding.
"""

s = bytes('café', encoding='utf8')
print(s[0]) # 返回0-255数值
print(s[:1]) # bytes类型

# s[1] = 22 # 修改失败，bytes为不可变类型

s_arr = bytearray(s)
print(s_arr)

print(s_arr[-1:]) # bytearray类型

s_arr[1] = 22
print(s_arr[1]) # 修改成，s_arr为可变类型

