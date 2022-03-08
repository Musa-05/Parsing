import random
import time
import os
import csv

import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}


# функция собирает все ссылки в TXT с названием жанра
def get_geners_urls():
    url = 'https://aldebaran.ru/knigi/'
    r = requests.get(url=url, headers=headers)

    # Создает папку если она не существует
    if not os.path.exists(f'data'):
        os.mkdir(f'data')

    soup = BeautifulSoup(r.text, 'lxml')
    # собирает все ссылки из главного раздела ВСЕ ЖАНРЫ
    urls_geners_list = []
    urls_geners = soup.find('div', class_='all_genres').find_all('li')
    for url in urls_geners:
        href = f"https://aldebaran.ru{url.find('a').get('href')}"
        urls_geners_list.append(href)

    # название для текстового файла
    for url_gener in urls_geners_list:
        file_name = url_gener.split("/")[-2]

        with open(f'data/{file_name}.txt', 'w', encoding='utf-8') as file:
            file.write('')

            # цикл проходит по всем страницам пагинации
            i = 1
            while True:

                url_pagenum = f'{url_gener}pagenum-{i}/'
                print(f'номер страницы {i} - {file_name}')
                r = requests.get(url=url_pagenum, headers=headers)
                time.sleep(random.randrange(1, 3))
                soup = BeautifulSoup(r.text, 'lxml')

                page_count = int(soup.find('div', class_='paginator').find('b').text)
                if page_count == 3:
                    break
                # собирает все ссылки на карточки товара
                items_books = soup.find('div', class_='wooklist').find_all('p', class_='booktitle')
                item_urls_list = []

                for item in items_books:
                    item_url = f"https://aldebaran.ru{item.find('a').get('href')}"
                    time.sleep(random.randrange(1, 3))
                    print(item_url)
                    item_urls_list.append(item_url)
                i += 1

                # сохраняет все ссылки в файл
                with open(f'data/{file_name}.txt', 'a', encoding='utf-8') as file:
                    for url in item_urls_list:
                        file.write(f'{url}\n')

# функция открывает все собранные ссылки из get_geners_urls и получает данные в формате CSV
def get_data():
    path = 'E:\PythonProect\Test_Parsing\data'
    list_file = os.listdir(path)
    list_data = []
    for i in list_file:
        list_data.append(i)

    for list_txt in list_data:
        with open(f'{path}\{list_txt}', encoding='utf-8') as file:
            urls_list = [url.strip() for url in file.readlines()]
        # создает CSV файл
        with open(f'data_csv\{list_txt.split(".")[0]}.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')

            writer.writerow(
                (
                    'Название книги',
                    'Автор',
                    'URL',
                    'Описание'
                )
            )
        count = 0
        # проходит по все ссылкам
        for url in urls_list:
            try:
                r = requests.get(url=url, headers=headers)
                time.sleep(2)
                soup = BeautifulSoup(r.text, 'lxml')
            except Exception as ex:
                continue

            try:
                book_name = soup.find('div', class_='item_title').find('h1').text.strip()
            except:
                book_name = None
            try:
                book_avtor = soup.find('div', class_='item_title').find('a').text.strip()
            except:
                book_avtor = None
            try:
                book_text = soup.find('div', class_='right_block').find('div',
                                                                        class_='navContainer').text.strip().replace(
                    '\t', '').replace('\n', ' ')
            except:
                book_text = None
            count += 1
            print(f'{count}')

            with open(f'data_csv\{list_txt.split(".")[0]}.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file, delimiter=';')

                writer.writerow(
                    (
                        book_name,
                        book_avtor,
                        url,
                        book_text
                    )
                )


def main():
    # get_geners_urls()
    get_data()


if __name__ == '__main__':
    main()
