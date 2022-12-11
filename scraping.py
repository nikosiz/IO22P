from selenium import webdriver
from bs4 import BeautifulSoup

from text_formatting import *


class PageType:
    MAIN = 0
    PRODUCT = 1


def set_web_driver_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')  # without opening browser window


def get_shop_offers_from_product_page(product_page):
    return product_page.find_all(class_='product-offers__list__item js_productOfferGroupItem')


def get_product_name(product_page):
    product_name_div = product_page.find(class_='product-top__title')
    try:
        product_name = product_name_div.getText()
    except:
        product_name = 'None'

    return product_name


def get_shop_name(shop_offer):
    info_div = shop_offer.find(class_='product-offer__container clickable-offer js_offer-container-click '
                                           'js_product-offer')
    return info_div['data-shopurl']


def get_product_price(shop_offer):
    info_div = shop_offer.find(class_='product-offer__container clickable-offer js_offer-container-click '
                                      'js_product-offer')
    return info_div['data-price']


def get_delivery_price(shop_offer):
    return 0


def extract_data_from_product_page(product_page):
    # TODO error handling
    data = []
    product_name = get_product_name(product_page).replace('\n', '')

    shop_offers = get_shop_offers_from_product_page(product_page)
    for shop_offer in shop_offers:
        shop_name = get_shop_name(shop_offer)
        product_price = get_product_price(shop_offer)
        delivery_price = get_delivery_price(shop_offer)
        offer = [product_name, shop_name, product_price, delivery_price]
        data.append(offer)

    return data


def get_product_click_hash(product):
    return product.find('a').get('href')


def extract_products_from_main_page(page):
    return page.find_all(class_='cat-prod-row__body')


def get_page_content(phrase, page_type):
    if page_type is PageType.MAIN:
        url = get_main_ceneo_page_url(phrase)
    else:
        url = get_product_page_url(phrase)

    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def get_product_offers(search_phrase):
    product_offers = []

    set_web_driver_options()

    main_ceneo_page = get_page_content(search_phrase, PageType.MAIN)
    products = extract_products_from_main_page(main_ceneo_page)

    for product in products:
        click_hash = get_product_click_hash(product)
        product_page = get_page_content(click_hash, PageType.PRODUCT)
        product_data = extract_data_from_product_page(product_page)
        product_offers += product_data

    return product_offers
