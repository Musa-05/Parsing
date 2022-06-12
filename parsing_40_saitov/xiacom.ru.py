import requests
from bs4 import BeautifulSoup
import csv
import time
import random

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'

}


# добавляет все ссылки в csv файл
def write_csv(url):
    with open('xiacom_links.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([url])


# удаляет дубли из csv файла
def write_set(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    seen_lines = set()
    with open(file_path, 'w') as file:
        for line in lines:
            if line not in seen_lines:
                seen_lines.add(line)
                file.write(line)


# возвращает HTML страницу
def get_html(url):
    res = requests.get(url=url, headers=HEADERS)
    random.randint(2, 7)
    # with open('index_pagination.html', 'w', encoding='utf-8') as file:
    #     file.write(res.text)
    # with open('index_pagination.html', encoding='utf-8') as file:
    #     src = file.read()
    return res.text


# возвращает ссылки на категории (каталог товаров)
def get_categories(html):
    soup = BeautifulSoup(html, 'lxml')
    categories = soup.find_all('div', class_='catalog-page__item-header')
    data = []
    for category in categories:
        url = f"https://xiacom.ru{category.find('a').get('href')}"
        data.append(url)
    return data


# возвращает страницу пагинации
def get_paginations(html):
    soup = BeautifulSoup(html, 'lxml')
    next_page = f"https://xiacom.ru{soup.find('a', class_='btn-common_more-btn').get('href')}"
    return next_page


# получает ссылки на катрочки товаров и сохраняет в CSV
def get_links(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find('div', class_='catalog-list').find_all('div', class_='compact-card__desc')
    for link in links:
        url = f"https://xiacom.ru{link.find('a').get('href')}"
        write_csv(url)
        # print(url)


def main():
    url = 'https://xiacom.ru/catalog/'
    html = get_html(url)
    categories = get_categories(html)
    for category in categories:
        html = get_html(category)
        while True:
            try:
                get_links(html)
                next_page = get_paginations(html)
                print(next_page)
                html = get_html(next_page)
            except:
                break

    write_set('xiacom_links.csv')


if __name__ == '__main__':
    main()
