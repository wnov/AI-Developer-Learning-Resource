"""
Cartesian product in a generattor expression.
"""

colors = ['black', 'white']
sizes = ['S', 'M', 'L']

# generator expresion 一次只生成1个对象，这样无需存储整个list，节省内存
for tshirt in (f'{c} {s}' for c in colors for s in sizes):
    print(tshirt)


