import json
import requests
from bs4 import BeautifulSoup
import time
import random

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}


def get_articl_url(url):
    r = requests.get(url=url, headers=headers)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(r.text)
    with open('index.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    page_count = int(soup.find('div', class_='col-md-12').find('span', class_='navigations').find_all('a')[-1].text)

    articls_urls_list = []

    for page in range(1, page_count + 1):
        res = requests.get(url=f'https://hi-tech.news/page/{page}/', headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        articl_urls = soup.find_all('a', class_='post-title-a')
        for ua in articl_urls:
            art_ul = ua.get('href')
            articls_urls_list.append(art_ul)

        time.sleep(random.randrange(2, 5))
    with open('articls_urls_list.txt', 'w', encoding='utf-8') as file:
        for url in articls_urls_list:
            file.write(f'{url}\n')


def get_data(file_path):
    with open(file_path, encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]

    result_data = []
    for url in urls_list:
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')

        article_title = soup.find('div', class_='post-content').find('h1', class_='title').text.strip()
        article_date = soup.find('div', class_='tile-views').text.strip()
        article_img = f"https://hi-tech.news{soup.find('div', class_='post-media-full').find('img').get('src')}"
        article_text = soup.find('div', class_='the-excerpt').text.strip().replace('\n', '')

        result_data.append(
            {
                'article_title': article_title,
                'article_date': article_date,
                'article_img': article_img,
                'article_text': article_text
            }
        )

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    get_articl_url('https://hi-tech.news/')
    get_data('articls_urls_list.txt')


if __name__ == '__main__':
    main()
