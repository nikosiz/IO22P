from selenium import webdriver
from bs4 import BeautifulSoup

from product_scraping import *
from driver_setting import set_web_driver_options
from text_formatting import *
from customized_sort import *
from helper_classes import *
from tqdm import tqdm


# main function in this module, called by main() in main module
# given product search phrase, returns ready basket
def get_product(search_phrases, sorting):
    basket = []
    #tqdm shows progress bar,
    for search_phrase in tqdm(search_phrases):
        products = get_product_offers(search_phrase)
        basket.append(products)

    if sorting == SortType.PRICE:
        return sort_by_price(basket)
    if sorting == SortType.SHOP_NUM:
        return sort_by_shop_num(basket)


# extracts data from every product (search phrase)
# and returns 10 best fitting product offer
def get_product_offers(search_phrase):
    product_offers = []

    main_ceneo_page = get_page_content(search_phrase, PageType.MAIN)
    products = extract_products_from_main_page(main_ceneo_page)

    # checking if request does not return any product
    if not products:
        return product_offers

    # scraping information about products on first main Ceneo page
    for product in products:
        product_offers += scrap_product_offers(product, search_phrase)
        if len(product_offers) >= 10:
            return product_offers

    # if number of offers is < 10
    # and there is more than one Ceneo page, repeat
    num_of_pages = get_num_of_pages(main_ceneo_page) + 1
    for i in range(1, num_of_pages, 1):
        next_ceneo_page = get_page_content(search_phrase, PageType.NEXT, i)

        next_products = extract_products_from_main_page(next_ceneo_page)
        for product in next_products:
            product_offers += scrap_product_offers(product, search_phrase)
            if len(product_offers) >= 10:
                return product_offers
    return product_offers


# if product has offers, function creates click  hash
# and scraps offers from product (product_scraping module)
def scrap_product_offers(product, search_phrase):
    if product_has_ceneo_offers(product):
        click_hash = get_product_click_hash(product)
        product_page = get_page_content(click_hash, PageType.PRODUCT)
        product_data = extract_data_from_product_page(product_page, search_phrase)
        return product_data
    else:
        return []


# depending on page type, returns soup object of page
def get_page_content(phrase, page_type, page_num=0):
    if page_type is PageType.MAIN:
        url = get_main_ceneo_page_url(phrase)
    elif page_type is PageType.NEXT:
        url = get_next_ceneo_page_url(phrase, page_num)
    else:
        url = get_product_page_url(phrase)

    driver = webdriver.Chrome(chrome_options=set_web_driver_options())
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


# returns number of products found by Ceneo
# divided by number of products per page
def get_num_of_pages(main_ceneo_page):
    products_per_page = 30
    sidebar_nav = main_ceneo_page.find(class_='grid-cat__site js_sidebar')
    quantity = sidebar_nav.find(class_='cat-nav__title__quantity').getText()
    num_of_all_products = int(quantity)
    num_of_pages = num_of_all_products // products_per_page
    return num_of_pages


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


def get_product_click_hash(product):
    return product.find('a').get('href')


def extract_products_from_main_page(page):
    return page.find_all(class_='cat-prod-row__body')
