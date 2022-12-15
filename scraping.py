from selenium import webdriver
from bs4 import BeautifulSoup

from text_formatting import *


class PageType:
    MAIN = 0
    PRODUCT = 1
    NEXT = 2


def set_web_driver_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')  # without opening browser window
    options.add_argument('no-sandbox')


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
    try:
        info_div = shop_offer.find(class_='product-offer__container clickable-offer js_offer-container-click '
                                          'js_product-offer')
        info = info_div['data-shopurl']
    except:
        info = 'None'
    return info


def get_product_price(shop_offer):
    try:
        info_div = shop_offer.find(class_='product-offer__container clickable-offer js_offer-container-click '
                                          'js_product-offer')
        info = info_div['data-price']
    except:
        info = 'None'
    return info


def get_delivery_price(shop_offer):
    return 'None'


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


def get_num_of_pages(main_ceneo_page):
    products_per_page = 30
    sidebar_nav = main_ceneo_page.find(class_='grid-cat__site js_sidebar')
    quantity = sidebar_nav.find(class_='cat-nav__title__quantity').getText()
    num_of_all_products = int(quantity)
    num_of_pages = num_of_all_products // products_per_page
    return num_of_pages


def get_page_content(phrase, page_type, page_num=0):
    if page_type is PageType.MAIN:
        url = get_main_ceneo_page_url(phrase)
    elif page_type is PageType.NEXT:
        url = get_next_ceneo_page_url(phrase, page_num)
    else:
        url = get_product_page_url(phrase)

    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


# checks if product redirects to allegro or has 0 offers (no shops under price)
# it is not necessary to scrap that page then
def product_has_ceneo_offers(product):
    price_div = product.find(class_='cat-prod-row__price')
    shop_number_div = price_div.find(class_='shop-numb')
    try:
        if shop_number_div.getText() == '':
            return False
        else:
            return True
    except:
        return False


def get_product_offers(search_phrase):
    product_offers = []

    set_web_driver_options()

    main_ceneo_page = get_page_content(search_phrase, PageType.MAIN)
    num_of_pages = get_num_of_pages(main_ceneo_page) + 1

    products = extract_products_from_main_page(main_ceneo_page)

    for product in products:
        if product_has_ceneo_offers(product):
            click_hash = get_product_click_hash(product)
            product_page = get_page_content(click_hash, PageType.PRODUCT)
            product_data = extract_data_from_product_page(product_page)
            product_offers += product_data

    # if there is more than one page, repeat
    for i in range(1, num_of_pages, 1):
        next_ceneo_page = get_page_content(search_phrase, PageType.NEXT, i)

        next_products = extract_products_from_main_page(next_ceneo_page)
        for product in next_products:
            if product_has_ceneo_offers(product):
                click_hash = get_product_click_hash(product)
                product_page = get_page_content(click_hash, PageType.PRODUCT)
                product_data = extract_data_from_product_page(product_page)
                product_offers += product_data

    return product_offers
