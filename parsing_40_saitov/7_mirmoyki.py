import requests
from bs4 import BeautifulSoup

import datetime
import random
import time
import csv

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'
}


# сбор ссылок в txt
def get_html(url):
    # res = requests.get(url=url, headers=HEADERS)
    # with open('index1.html', 'w', encoding='utf-8') as file:
    #     file.write(res.text)
    with open('index1.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    item_urls_list = []

    page_count = int(soup.find('div', class_='catalog-pagination').find_all('a')[-2].text)
    for page in range(1, page_count + 1):
        print(page)
        url = f'https://mirmoyki.ru/shop/folder/moyki/?PAGEN_1={page}'
        req = requests.get(url=url, headers=HEADERS)
        time.sleep(random.randint(2, 7))
        # with open('index2.html', 'w', encoding='utf-8') as file:
        #     file.write(req.text)
        # with open('index1.html', encoding='utf-8') as file:
        #     src = file.read()

        soup = BeautifulSoup(req.text, 'lxml')
        items = soup.find_all('div', class_='products-flex-item')
        for item in items:
            item_url = f"https://mirmoyki.ru{item.find('a').get('href')}"
            item_urls_list.append(item_url)

    with open('item_urls_list.txt', 'w', encoding='utf-8') as file:
        for url in item_urls_list:
            file.write(url + '\n')

        # print(page_count)


# функция для сохранения заголовок
FILENAME = 'MIR.csv'


def create_csv(filename, order):
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=order, delimiter=';').writeheader()


def write_csv(filename, data):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        csv.DictWriter(file, fieldnames=list(data), delimiter=';').writerow(data)


def get_data(file_path):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    with open(file_path, encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]
    count = 0
    for url in urls_list:
        r = requests.get(url=url, headers=HEADERS)
        count += 1
        print(count)

        time.sleep(random.randint(3, 8))
        # with open('page_item.html', 'w', encoding='utf-8') as file:
        #     file.write(r.text)
        # with open('page_item.html', encoding='utf-8') as file:
        #     src = file.read()
        soup = BeautifulSoup(r.text, 'lxml')

        try:
            name = soup.find('div', class_='product-info').find('h1').text
        except:
            name = ''
        try:
            price = soup.find('div', class_='product-info').find('div', class_='product-price').text.strip()
        except:
            price = ''
        try:
            description = soup.find('div', class_='product-accordion-tabs').find('div', class_='accordion-content').text.strip().replace('\t', '').replace('\n', '')
        except:
            description = ''

        try:
            image = soup.find('div', class_='owl-carousel').find_all('a')
        except:
            image = ''
        image = '\n'.join([f"https://mirmoyki.ru{i.get('href')}" for i in image])

        data = {
            'url': url,
            'name': name,
            'price': price,
            'description': description,
            'image': image
        }
        order = ['url', 'name', 'price', 'description', 'image']

        try:
            characteristic = soup.find('div', class_='product-specification').find_all('tr')
        except:
            characteristic = ''
        for char in characteristic:
            char_key = char.find_all('td')[0].text
            char_value = char.find_all('td')[1].text
            order.append(char_key)
            data[char_key] = char_value


        write_csv(FILENAME, data)




def main():

    order = ['url', 'name', 'price', 'description', 'image', 'Производитель',  'Артикул', 'Материал изготовления', 'Форма мойки', 'Страна', 'Тип монтажа', 'Размеры (ДхШ)']
    create_csv(FILENAME, order)
    # get_html('https://mirmoyki.ru/shop/folder/moyki/')
    get_data(file_path='item_urls_list.txt')



if __name__ == '__main__':
    main()
