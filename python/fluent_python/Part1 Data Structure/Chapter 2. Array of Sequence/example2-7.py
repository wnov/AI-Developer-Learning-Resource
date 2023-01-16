"""
Tuple as record.
"""

# 作为record的tuple内容的顺序决定了其对应的字段，例如33.9425表示维度，-118.408056表示经度
lax_coordinates = (33.9425, -118.408056)
city, year, pop, chg, area = ('Tokyo', 2003, 32_450, 0.66, 8014)
traveler_ids = [('USA', '311195855'), ('BRA', 'CEE342567'), ('ESP', 'XDA205856')]

for passport in sorted(traveler_ids):
    print('%s/%s' % passport)

for country, _ in traveler_ids:
    print(country)


