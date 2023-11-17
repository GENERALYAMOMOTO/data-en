import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://ekb.pulscen.ru/price/3201-specodezhda'
parsed_data = []

for page in range(1, 11): 
    url = f'{base_url}?page={page}'
    response = requests.get(url)
    html_code = response.text

    soup = BeautifulSoup(html_code, 'html.parser')

    objects = soup.find_all('li', class_='product-listing__item')

    for obj in objects:
        product_name_elem = obj.find('span', class_='product-listing__product-name')
        product_name = product_name_elem.text.strip() if product_name_elem else ''

        product_price_elem = obj.find('i', class_='bp-price')
        product_price = product_price_elem.text.strip() if product_price_elem else ''

        availability_elem = obj.find('li', class_='product-listing__price-info-item_available')
        availability = availability_elem.text.strip() if availability_elem else ''

        company_name_elem = obj.find('span', class_='product-listing__company-name')
        company_name = company_name_elem.text.strip() if company_name_elem else ''

        company_info_elem = obj.find('li', class_='product-listing__company-info-item')
        company_info = company_info_elem.text.strip() if company_info_elem else ''

        company_location_elem = obj.find('div', class_='product-listing__company-info-region')
        company_location = company_location_elem.text.strip() if company_location_elem else ''

        contact_number_elem = obj.find('span', class_='js-show-phone-number')
        contact_number = contact_number_elem.text.strip() if contact_number_elem else ''

        data = {
            'product_name': product_name,
            'product_price': product_price,
            'availability': availability,
            'company_name': company_name,
            'company_info': company_info,
            'company_location': company_location,
            'contact_number': contact_number,
        }
        parsed_data.append(data)

parsed_data_sorted = sorted(parsed_data, key=lambda x: x['product_name'])
parsed_data = sorted(parsed_data, key=lambda x: float(x['product_price'].replace(' руб.', '').replace(' ', '')))

with open('parsed_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(parsed_data, json_file, ensure_ascii=False, indent=4)

for data in parsed_data:
    print(data)
