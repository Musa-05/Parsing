import requests
from bs4 import BeautifulSoup

import datetime
import time
import csv
import random
import json

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}


def get_urls(url):
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    page_coutn = int(soup.find('div', class_='pager').find_all('span', class_='item')[-1].text.strip())

    item_urls_list = []
    for i in range(1, page_coutn + 1):
        r = requests.get(f'https://www.olx.ua/detskiy-mir/?page={i}', headers=headers)
        time.sleep(random.randrange(2, 5))
        soup = BeautifulSoup(r.text, 'lxml')
        items = soup.find('table', class_='fixed offers breakword redesigned').find_all('tr')

        for item in items:
            try:
                item_url = item.find('td').find('a', class_='marginright5').get('href')

            except Exception as ex:
                continue
            item_urls_list.append(item_url)

        print(i)
    with open('item_urls_list.txt', 'w', encoding='utf-8') as file:
        for url in item_urls_list:
            file.write(url + '\n')


def get_data(file_path):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    with open(f'labirint_{cur_time}.csv', 'w', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=";")

        writer.writerow(
            (
                'Ссылка',
                'Дата публикации',
                'Заголовок',
                'Цена',
                'Имя'
            )
        )

    with open(file_path, encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]

    result_data = []
    count = 0
    for url in urls_list:
        r = requests.get(url=url, headers=headers)
        time.sleep(random.randrange(2, 5))
        soup = BeautifulSoup(r.text, 'lxml')

        try:
            data_publication = soup.find('span', class_='css-ubdo89-Text').find('span',
                                                                                class_='css-19yf5ek').text.strip()
        except:
            data_publication = 'Нет даты'
        try:
            title_publication = soup.find('h1').text
        except:
            title_publication = 'Нет заголовка'
        try:
            price_publication = soup.find('div', class_='css-dcwlyx').text.strip().replace('\"', '')
        except:
            price_publication = 'Нет цены'
        try:
            name_publication = soup.find('h2').text.strip()
        except:
            name_publication = 'Имя не указана'

        result_data.append(
            {
                'url': url,
                'data_publication': data_publication,
                'title_publication': title_publication,
                'price_publication': price_publication,
                'name_publication': name_publication,

            }
        )
        with open(f'labirint_{cur_time}.csv', 'a', encoding='cp1251', newline='') as file:
            writer = csv.writer(file, delimiter=';')

            writer.writerow(
                (
                    url,
                    data_publication,
                    title_publication,
                    price_publication,
                    name_publication
                )
            )

    count += 1
    print(count)
    with open(f'result_data_{cur_time}.json', 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    get_urls('https://www.olx.ua/detskiy-mir/')
    get_data(file_path='item_urls_list.txt')


if __name__ == '__main__':
    main()
