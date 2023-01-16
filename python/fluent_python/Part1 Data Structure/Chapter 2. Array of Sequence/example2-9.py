"""
match/case语句中使用模式匹配, python3.10以后的特征
"""

def handle_command(self, message):
    match message:
        case ['BEEPER', frequency, times]:
            self.beep(times, frequency)
        case ['NECK', angle]:
            self.rotate_neck(angle)
        case ['LED', ident, intensity]:
            self.leds[ident].set_brightness(ident, intensity)
        case ['LED', ident, red, green, blue]:
            self.leds[ident].set_color(ident, red, green, blue)
        case _:
            raise InvalidCommand(message)


metro_areas = [
('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

"""
使用match/case表达式, 解构嵌套tuple
"""
from __future__ import annotations
from typing import Union, Tuple, Callable
def main() -> Callable[...]:
    print(f'{"":15} | {"latitude":>9} | {"longitude":>9}')
    for record in metro_areas:
        match record:
            case [name, _, _, (lat, lon)] if lon <= 0:
                print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')

"""
str , bytes和bytearray等不是sequence, 使用match/case时必须先转换为tuple
"""
match tuple(phone):
    case ['1', *rest]: # North America and Caribbean
        ...
    case ['2', *rest]: # Africa and some territories
        ...
    case ['3' | '4', *rest]: # Europe
        ...

    case [name, _, _, (lat, lon) as coord]: # 直接生成新tuple coord
        ...
    case [str(name), _, _, (float(lat), float(lon))]: # 对变量进行类型检查，这样可以进行更准确的匹配
        ...
