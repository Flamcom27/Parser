#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

URL = 'https://auto.ria.com/search/?indexName=auto,order_auto,newauto_search&brand.id[0]=84&price.currency=1&abroad.not=0&custom.not=1&country.import.usa.not=-1&page=0&size=10'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'accept': '*/*'
}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params) 
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('section', class_='ticket-item')
    cars = []
    for item in items:
        title = item.find('a', class_='address').get_text().strip()
        year = title[-4:]
        cars.append({
            'title': title[0:-5].strip(),
            'link': item.find('a', class_='address').get('href'),
            'price': item.find('span', class_='bold green size22').get_text().strip(),
            'year': year,
            'city': item.find('li', class_='item-char view-location js-location').get_text().replace(' ( от )', '').strip()
        })
    return cars

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html.text)
    else:
        print('Error')


if __name__ == '__main__':
    parse()
