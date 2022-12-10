from bs4 import BeautifulSoup
from selenium import webdriver


def set_web_driver_options():
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')


def change_search_text_to_url(search_text):
    template = 'https://www.ceneo.pl/Zabawki;szukaj-{}'
    search_term = search_text.replace(' ', '+')
    return template.format(search_term)


def extract_data_from_results(results):
    data = []
    for search_result in results:
        product_name_div = search_result.find(class_='cat-prod-row__name')
        product_name = product_name_div.find('span')
        data += product_name
        price_div = search_result.find(class_='cat-prod-row__price')
        price = price_div.find(class_='value')
        data += price
    return data


def extract_page_content(url):
    driver = webdriver.Firefox()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def main(search_text):
    set_web_driver_options()

    url = change_search_text_to_url(search_text)
    page_content = extract_page_content(url)

    products = page_content.find_all(class_='cat-prod-row__body')
    data = extract_data_from_results(products)

    for product_name in data:
        print(product_name)


main('klocki lego minecraft')
