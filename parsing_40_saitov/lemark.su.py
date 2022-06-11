import requests
from bs4 import BeautifulSoup
import csv
import time
import random

HEADERS = {

    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',

}


def get_url(url):
    res = requests.get(url=url, headers=HEADERS)
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(res.text)
    # with open('index.html', encoding='utf-8') as file:
    #     src = file.read()
    catalog_url_list = []

    soup = BeautifulSoup(res.text, 'lxml')
    page_count = int(soup.find('div', class_='pages').find('a', class_='last-page').get('href').split('=')[-1])
    for page in range(1, page_count + 1):
        url_page = f'https://www.river-amico.ru/catalog/men_auto/?PAGEN_1={page}'
        res = requests.get(url=url_page, headers=HEADERS)
        time.sleep(2)
        soup = BeautifulSoup(res.text, 'lxml')

        # сбор ссылок
        catalog_men_automatic = soup.find_all('div', class_='catalog-box catalog-close')
        for url in catalog_men_automatic:
            catalog_url = f"https://www.river-amico.ru{url.find('a').get('href')}"
            catalog_url_list.append(catalog_url)
            print(catalog_url)

    with open('urls.txt', 'w', encoding='utf-8') as file:
        for url in catalog_url_list:
            file.write(f'{url}\n')


def get_data(file_data):
    # with open(file_data, encoding='utf-8') as file:
    #     file_urls = file.readlines()[:1]
    #     for url in file_urls:
            # print(url)
            # r = requests.get(url=url, headers=HEADERS)
            # with open('file_index.html', 'w', encoding='utf-8') as file:
            #     file.write(r.text)
            with open('file_index.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

            items = soup.find('div', class_='menu-line')
            print(soup)





# def main():
    # get_url('https://www.river-amico.ru/catalog/men_auto/')
    # get_data('urls.txt')


# if __name__ == '__main__':
#     main()
