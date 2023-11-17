import os
import re
import statistics
import json
from zipfile import ZipFile
from bs4 import BeautifulSoup

result = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

def file_read(file_name):
    soup = BeautifulSoup(file_name, 'html.parser')
    prods = soup.find_all('div', attrs={'class': 'product-item'})
    # print(prod)

    for prod in prods:
        item = {}            
        item['id'] = prod.a['data-id']
        item['link'] = prod.find_all('a')[1]['href']
        item['img'] = prod.find_all('img')[0]['src']
        item['name'] = prod.find_all('span')[0].get_text().strip()
        item['price'] = int(prod.find_all('price')[0].get_text().replace('₽', '').replace(' ', '').strip())
        item['bonus'] = int(prod.find_all('strong')[0].get_text().replace('+ начислим', '').replace(' бонусов', '').strip())

        props = prod.ul.find_all('li')
        for prop in props:
            item[prop['type']] = prop.get_text().strip()
        items.append(item)
    return items


max_file = 40
items = []
with ZipFile("zip_var_45.zip", "r") as zip_ref:
    file_list = zip_ref.namelist()

    for filename in file_list:
        with zip_ref.open(filename) as file:
            html_content = file.read()
            file_read(html_content)

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open(os.path.join(result, os.path.normpath("res_2_sort.json")), 'w') as f:
    f.write(json.dumps(items, ensure_ascii=False))

filter_views = []
for product in items:
    if product['bonus'] >= 1000:
        filter_views.append(product)

with open(os.path.join(result, os.path.normpath("res_2_filter.json")), 'w') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))

all_price = {}
camera = {'no_camera': 0}
all_price['sum_price'] = 0
all_price['min_price'] = 10 ** 9 + 1
all_price['max_price'] = 0
std_price = [0]
for product in items:
    temp = product['price']
    all_price['sum_price'] += temp
    if all_price['min_price'] > temp:
        all_price['min_price'] = temp
    if all_price['max_price'] < temp:
        all_price['max_price'] = temp
    std_price.append(temp)
    if product.get('camera', False) != False:
        if product['camera'] in camera:
            camera[product['camera']] += 1
        else:
            camera[product['camera']] = 1
    else:
        camera['no_camera'] += 1
all_price['avr_price'] = all_price['sum_price'] / len(items)
all_price['std_price'] = statistics.stdev(std_price)

with open(os.path.join(result, os.path.normpath("res_2_charact.json")), 'w') as f:
    f.write(json.dumps(all_price, ensure_ascii=False))
    f.write(json.dumps(camera, ensure_ascii=False))