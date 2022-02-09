import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}


def get_data(url):
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    item_block = soup.find('div', class_='curtable').find_all('tr')

    data_list = []
    for item in item_block:
        try:
            block_value = item.find('td', class_='value').next_element
        except:
            block_value = 'no'

        data_list.append(block_value)
    print(data_list[107])


def main():
    get_data('https://tables.finance.ua/ru/currency/mastercard')


if __name__ == '__main__':
    main()
