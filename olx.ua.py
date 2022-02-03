import requests
from bs4 import BeautifulSoup
import time
import csv
import random

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}


def get_urls_data(url):
    # r = requests.get(url=url, headers=headers)
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(r.text)
    # with open('index.html', encoding='utf-8') as file:
    #     src = file.read()
    #
    # soup = BeautifulSoup(src, 'lxml')
    # main_headings = soup.find('div', class_='maincategories')
    # main_urls = main_headings.find_all('div', class_='li fleft')
    # main_urls_list = []
    # for item in main_urls:
    #     main_url = item.find('a').get('href')
    #     main_urls_list.append(main_url)

    # for main_url in main_urls_list[:1]:
    #     r = requests.get(url=main_url, headers=headers)
    #     soup = BeautifulSoup(r.text, 'lxml')
    #     rubrika_urls = soup.find('div', class_='toplinks').find('div', class_='inner').find_all('ul')
    #
    #
    #     urls_rubrik = []
    #     for rubrika in rubrika_urls:
    #         #url_rubrik = rubrika.find('a').get('href')
    #         try:
    #             urls_rubrik1 = rubrika.find_all('li', class_='visible')[0].find('a').get('href')
    #             urls_rubrik2 = rubrika.find_all('li', class_='visible')[1].find('a').get('href')
    #             urls_rubrik.append(urls_rubrik1)
    #             urls_rubrik.append(urls_rubrik2)
    #         except:
    #             urls_rubrik = 'no'
    #
    #     for url in urls_rubrik[:1]:
    #         r = requests.get(url=url, headers=headers)
    #         with open('index2.html', 'w', encoding='utf-8') as file:
    #             file.write(r.text)

    with open('../PythonProect/lesson_8/index2.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    all_block = soup.find('table', class_='fixed offers breakword redesigned').find('tbody').find_all('tr', class_='wrap')
    for item in all_block:
        item_url = item.find('td', class_='photo-cell').find('a').get('href')


        print(item_url)


def main():
    get_urls_data('https://www.olx.ua/')


if __name__ == '__main__':
    main()
