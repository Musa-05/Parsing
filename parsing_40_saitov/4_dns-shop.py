from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep
import random
import csv

options = webdriver.ChromeOptions()
options.add_argument(
    'User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36')
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path='E:\PythonProect\parsing_DNS\chromedriver.exe', options=options)


def get_urls(url):
    with open('dns.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        writer.writerow(
            (
                'Название',
                'Цена',
                'URL',
                'Изображение',
                'Описание',

            )
        )

    # получаем все ссылки на карточки
    try:
        driver.get(url=url)
        sleep(random.randrange(7, 10))
        driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/button[1]').click()
        sleep(random.randrange(3, 7))

        driver.execute_script("window.scrollTo(0, 4500);")
        sleep(random.randrange(3, 5))

        page_count = driver.find_element(By.CLASS_NAME, 'pagination-widget__pages').find_elements(By.CLASS_NAME,
                                                                                                  'pagination-widget__page ')
        sleep(random.randrange(2, 4))
        page_count_int = len(page_count)

        urls_product_list = []
        for page in range(1, 13):
            url = f'https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/?p={page}'
            driver.get(url)
            sleep(random.randrange(2, 5))
            driver.execute_script("window.scrollTo(0, 4000);")
            sleep(random.randrange(2, 5))

            all_product = driver.find_elements(By.CLASS_NAME, 'catalog-product__name')

            for item in all_product:
                url_product = item.get_attribute('href')
                sleep(random.randrange(2, 5))
                urls_product_list.append(url_product)
        sleep(random.randrange(5, 8))
        with open('urls_product_list.txt', 'w', encoding='utf-8') as file:
            for url in urls_product_list:
                file.write(url + '\n')


    except Exception as ex:
        print(ex)
    # finally:
    #     driver.close()
    #     driver.quit()


def get_data(file_path):
    sleep(10)
    try:
        with open(file_path, encoding='utf-8') as file:
            urls = file.readlines()

            count = 0
            for url in urls:
                driver.get(url)
                sleep(random.randrange(4, 8))

                try:
                    title_product = driver.find_element(By.CLASS_NAME, 'product-card-top__title').text.strip()
                except:
                    title_product = 'no title'

                try:
                    price_product = driver.find_element(By.CLASS_NAME, 'product-card-top__buy').find_element(
                        By.CLASS_NAME, 'product-buy__price').text.rstrip(' ?')
                except:
                    price_product = 'no price'
                try:
                    text_product = driver.find_element(By.CLASS_NAME, 'product-card-description-text').text.replace(
                        'Описание', '').strip()
                except:
                    text_product = 'no text'

                    sleep(2)

                driver.find_element(By.CLASS_NAME, 'tns-slide-active').click()

                sleep(2)
                img_items = driver.find_elements(By.CLASS_NAME, 'media-viewer-image__slider-item')
                sleep(5)

                img_urls = []

                for img in img_items[:3]:
                    img.find_element(By.TAG_NAME, 'img').click()
                    sleep(random.randrange(2, 4))
                    img_product_url = driver.find_element(By.CLASS_NAME, 'media-viewer-image__img-wrap').find_element(
                        By.TAG_NAME, 'img').get_attribute('src').strip()
                    sleep(random.randrange(2, 7))
                    img_urls.append(img_product_url)
                    sleep(2)

                count += 1
                print(count)

                with open('dns.csv', 'a', encoding='UTF-8', newline='') as files:
                    writer = csv.writer(files, delimiter=';')
                    writer.writerow(
                        (

                            title_product,
                            price_product,
                            url.strip(),
                            img_urls[0],
                            text_product.strip(),

                        )
                    )
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_urls('https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/')
    get_data('urls_product_list.txt')


if __name__ == '__main__':
    main()
