import requests
from bs4 import BeautifulSoup

import random
import re
import time
import json
import datetime

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}
def get_data(url):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%m')
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    page_count = int(soup.find('div', class_='base-pagination-wrapper').find_all('button')[-1].text)
    all_items_list = []
    for i in range(1, page_count + 1):
        url = f'https://m.sima-land.ru/rulonnye-shtory/p{i}/?c_id=45690&per-page=20&sort=price&viewtype=cards'
        r = requests.get(url=url, headers=headers)
        time.sleep(random.randrange(2, 5))
        soup = BeautifulSoup(r.text, 'lxml')
        all_items = soup.find('div', class_='N3Azx')

        urls_data_list = []
        for item in all_items:
            urls_item = 'https://m.sima-land.ru' + item.find('a').get('href')
            urls_data_list.append(urls_item)

        for urls_data in urls_data_list:
            res = requests.get(url=urls_data, headers=headers)

            soup = BeautifulSoup(res.text, 'lxml')

            all_list = []

            all_url = soup.find('div', class_='mMUuX')
            name = all_url.find('div', class_='utwuJ ytr0E').find('h1').text
            price = all_url.find('div', class_='rP6c0').find('span').text.replace('₽', '')
            price = re.sub(r'\s', '', price)

            all_list.append(
                {
                    'Имя продукта': name,
                    'Цена': price
                }
            )

            try:
                items_container = all_url.find('div', class_='items-container')
            except:
                items_container = 'no'

            try:

                marka = items_container.find_all('div', class_='item NfqAl')[0].text
            except:
                marka = 'no'

            try:
                articul = items_container.find_all('div', class_='item NfqAl')[1].text
            except:
                articul = 'no'

            try:
                certificat = items_container.find_all('div', class_='item NfqAl')[2].text
            except:
                certificat = 'no'

            try:
                ctrana = items_container.find_all('div', class_='item NfqAl')[3].text
            except:
                ctrana = 'no'

            try:
                coctav = items_container.find_all('div', class_='item NfqAl')[4].text.replace('\"', '')
            except:
                coctav = 'no'

            all_items_list.append(
                {
                    'Marka': marka,
                    'Artikul': articul,
                    'Certificat': certificat,
                    'Ctrana': ctrana,
                    'Coctav': coctav,
                    'all_list': all_list
                }
            )

    with open(f'data_{cur_time}.json', 'w', encoding='utf-8') as file:
        json.dump(all_items_list, file, indent=4, ensure_ascii=False)


def main():
    get_data('https://m.sima-land.ru/rulonnye-shtory/?c_id=45690&per-page=20&sort=price&viewtype=cards')


if __name__ == '__main__':
    main()
