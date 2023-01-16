"""
Unpacking nested tuples to access the longitude.
"""
import dis

t = (1, 2, [30, 40])
t[-1].append(123)
print(t)
dis.dis('t += [12]')

metro_areas = [
('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

def main():
    print(f'{"":15} | {"latitude":>9} | {"longitude":>9}') # >指定右对齐，字符串默认左对齐，数字默认右对齐，:+数字，指定字符串长度，不够的补空格
    for name, _, _, (lat, lon) in metro_areas: # unpack嵌套的tuple
        if (lon <= 0):
            print((f'{name:15} | {lat:9.4f} | {lon:9.4f}'))

if __name__ == '__main__':
    main()


