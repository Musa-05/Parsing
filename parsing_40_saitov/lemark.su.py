import requests
from bs4 import BeautifulSoup
import csv
import time

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
}
SITE = 'https://www.lemark.su'


def get_html(url):
    # res = requests.get(url=url, headers=HEADERS)
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(res.text)
    with open('index.html', encoding='utf-8') as file:
        src = file.read()
    return src


def get_links(html):
    soup = BeautifulSoup(html, 'lxml')
    item_urls_list = []
    items = soup.find_all('div', class_='product-item')
    for item in items:
        item_url = SITE + item.find('a').get('href')
        item_urls_list.append(item_url)
        print(item_url)

    with open('urls.txt', 'a', encoding='utf-8') as file:
        for url in item_urls_list:
            file.write(f'{url}\n')


def get_data(file_url):
    with open(file_url, encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]

    for url in urls_list[:1]:
        # res = requests.get(url=url, headers=HEADERS)
        # with open('index_page.html', 'w', encoding='utf-8') as file:
        #     file.write(res.text)
        with open('index_page.html', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        titel = soup.find('h1').text.strip()
        articul = soup.find('div', class_='goods-vendor').text.strip().replace('Артикул', '').strip()
        series = soup.find('div', class_='goods-series').text.replace('Серия:', '').strip()






def main():
    # urls = ['https://www.lemark.su/catalog/dlya_kukhni/', 'https://www.lemark.su/catalog/dlya_vannoy_komnaty/', 'https://www.lemark.su/catalog/aksessuary/']
    # url = 'https://www.lemark.su/catalog/dlya_kukhni/filter/clear/apply/?SHOWALL_1=1'
    # html = get_html(url)
    # get_html(html)
    # get_links(html)
    get_data('urls.txt')


if __name__ == '__main__':
    main()
