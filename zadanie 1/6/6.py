import requests
import json

url = 'https://www.cbr-xml-daily.ru/latest.js'
response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.text)

    html_output = '<ul>'
    for currency, rate in data['rates'].items():
        if rate < 0.02:  
            html_output += f'<li>{currency}: {rate}</li>'
    html_output += '</ul>'

    print(html_output)

    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(html_output)
else:
    print(f"Error {response.status_code}: {response.text}")
