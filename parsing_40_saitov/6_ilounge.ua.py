import requests
from bs4 import BeautifulSoup

import random
import time
import csv
import os

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}


def get_urls(url):
    r = requests.get(url=url, headers=headers)
    time.sleep(random.randrange(2, 4))

    file_name = url.split('/')[-1]
    if not os.path.exists(f'{file_name}'):
        os.mkdir(f'{file_name}')
    time.sleep(2)

    soup = BeautifulSoup(r.text, 'lxml')
    technology_apple = soup.find('div', class_='tile-row').find_all('div', class_='tile-content')

    # Техника Apple (собираем ссылки с главной страницы)
    technology_apple_urls = []
    for e in technology_apple:
        item_urls = f"https://ilounge.ua/{e.find('a').get('href')}"
        technology_apple_urls.append(item_urls)

    count = 0

    for apple_url in technology_apple_urls[12:-1]:

        r = requests.get(url=apple_url, headers=headers)
        time.sleep(random.randrange(2, 4))

        soup = BeautifulSoup(r.text, 'lxml')

        try:
            page_count = int(soup.find('div', class_='pagination').find_all('a')[-2].text)
        except:
            page_count = 1

        # проходим по пагинации страниц
        file_item_name = apple_url.split('/')[-1].replace('-', '_')

        for i in range(1, page_count + 1):
            try:
                r = requests.get(url=f'{apple_url}?page={i}', headers=headers)
                time.sleep(random.randrange(2, 4))
            except Exception as ex:
                print(ex)

            soup = BeautifulSoup(r.text, 'lxml')

            try:
                items = soup.find('ul', class_='tiny_products').find_all('li', class_='product')
                time.sleep(2)
            except:
                items = None

            # собрали все ссылки на карточки товаров
            items_urls_list = []

            for url in items:
                try:
                    item_url = f"https://ilounge.ua/{url.find('div', class_='product_info').find('a').get('href')}"
                except:
                    item_url = None
                items_urls_list.append(item_url)

            # file_item_name = apple_url.split('/')[-1]

            with open(f'{file_name}/{file_item_name}.txt', 'a', encoding='utf-8') as file:
                for url in items_urls_list:
                    file.write(f'{url}\n')
        count += 1
        print(f'{count} {file_item_name}')


def get_data(file_path):
    global list_txt
    list_file = os.listdir(file_path)
    if not os.path.exists('data_csv'):
        os.mkdir('data_csv')

    with open(r"data_csv\all_data.csv", 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                'Артикул',
                'Название (RU)',
                'Бренд',
                'Раздел',
                'Цена',
                'Старая цена',
                'Наличие',
                'Фото',
                'Фото gif',
                'Текст gif',
                'Ссылка',
                'Описание товара (RU)'

            )
        )

    list_name_files_txt = []
    count = 0
    for i in list_file:
        list_name_files_txt.append(i)
    for list_txt in list_name_files_txt:
        with open(f'{file_path}\{list_txt}', encoding='utf-8') as file:
            urls_list = [url.strip() for url in file.readlines()]

        # создаем csv файл

        # проходит по всем ссылкам

        for link in urls_list:
            r = requests.get(url=link, headers=headers)
            time.sleep(random.randrange(4, 7))
            # #soup = BeautifulSoup(r.text, 'lxml')
            # with open('ind.html', 'w', encoding='utf-8') as file:
            #     file.write(r.text)
            # with open('ind.html', encoding='utf-8') as file:
            #     src = file.read()

            soup = BeautifulSoup(r.text, 'lxml')

            # собираем все данные с каждого товара
            #   TODO необходимо проверить kod на других страницах
            try:
                articul = soup.find('div', class_='mpn').text.strip().split()[-1]

            except:
                articul = None

            try:
                name = soup.find('h1').text.strip()
            except:
                name = None

            try:
                brand = soup.find('a', class_='product-brand').find('img').get('alt').split()[1].strip()
            except:
                brand = None

            try:
                chapter = soup.find('div', id='path').text.replace('\n', '').split('|')[1:3]
                chapter = ' -'.join(chapter)
            except:
                chapter = None
            print(chapter)

            try:
                price = soup.find('div', class_='prices').text.strip().replace(' ₴', '')
            except:
                price = None

            try:
                price_old = soup.find('div', class_='compare_price').text.strip().replace(' ₴', '')
            except:
                price_old = None

            try:
                in_stok = soup.find('div', class_='stock-info instock-info').text.split()[0:2]
                in_stok = ' '.join(in_stok)
            except:
                in_stok = None

            try:
                images = soup.find('div', class_='images').find_all('li')
                images = '\n'.join([url.find('a').get('href') for url in images])
            except:
                images = None

            # Todo исключить не найденные картинки None
            try:
                img_gif = soup.find_all('tbody')
                img_gif = '\n'.join(
                    [f"https://ilounge.ua{img.find_next('img').get('data-original')}" for img in img_gif])
            except:
                img_gif = None

            try:
                text_gif = soup.find_all('tbody')[1:-1]
                text_gif = '\n\n'.join([text_all.find_next('p').text for text_all in text_gif])
            except:
                text_gif = None

            try:
                description = soup.find('div', class_='productdesc').text.strip()
            except:
                description = None

            with open(r"data_csv\all_data.csv", 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    (
                        articul,
                        name,
                        brand,
                        chapter,
                        price,
                        price_old,
                        in_stok,
                        images,
                        img_gif,
                        text_gif,
                        link,
                        description,

                    )
                )
        count += 1
        print(f'{count}')
    # with open(f"data_csv\{list_txt.split('.')[0]}.csv", 'w', encoding='utf-8', newline='') as file:
    #     writer = csv.writer(file, delimiter=';')
    #     writer.writerow(
    #         (
    #             'Артикул',
    #             'Название (RU)',
    #             'Бренд',
    #             'Раздел',
    #             'Цена',
    #             'Старая цена',
    #             'Наличие',
    #             'Фото',
    #             'Фото gif',
    #             'Текст gif',
    #             'Ссылка',
    #             'Описание товара (RU)'
    #
    #         )
    #     )


def main():
    # get_urls('https://ilounge.ua/catalog/apple')
    get_data(r'E:\PythonProect\Test_Parsing\apple')


if __name__ == '__main__':
    main()
