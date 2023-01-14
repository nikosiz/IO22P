from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

from text_formatting import *
from customized_sort import *


class PageType:
    MAIN = 0
    PRODUCT = 1
    NEXT = 2


delivery_price_list = []


def set_web_driver_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless=chrome')  # without opening browser window
    options.add_argument('no-sandbox')
    options.add_argument("user-agent=Chrome/80.0.3987.132")
    options.add_argument("--window-size=1920,1080")
    return options


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


def get_delivery_price():
    try:
        return delivery_price_list[0]
    finally:
        delivery_price_list.pop(0)


def get_shop_url(shop_offer):
    try:
        info_div = shop_offer.find(class_='product-offer__container clickable-offer js_offer-container-click '
                                          'js_product-offer')
        info = info_div['data-click-url']
        info = 'https://www.ceneo.pl' + info
    except:
        info = 'None'
    return info


def get_thumbnail_url(product_page):
    try:
        info_div = product_page.find(class_='js_gallery-media gallery-carousel__media')
        info = info_div.get('src')
    except:
        info = 'None'
    return info


def offer_has_every_information(offer):
    for information in offer:
        if offer[information] == 'None':
            return False
    for information_ in offer['resultProduct']:
        if offer['resultProduct'][information_] == 'None':
            return False
    for information__ in offer['resultProduct']['offer']:
        if offer['resultProduct']['offer'][information__] == 'None':
            return False
    return True


def extract_data_from_product_page(product_page, search_phrase):
    # TODO error handling
    data = []
    product_name = get_product_name(product_page).replace('\n', '')

    thumbnailUrl = get_thumbnail_url(product_page)

    shop_offers = get_shop_offers_from_product_page(product_page)
    for shop_offer in shop_offers:
        shop_name = get_shop_name(shop_offer)
        product_price = get_product_price(shop_offer)
        delivery_price = 0.0
        shop_url = get_shop_url(shop_offer)
        offer = {'searchProduct': search_phrase, "resultProduct": {"name": product_name, "thumbnailUrl": thumbnailUrl,
                                                                   "offer": {
                                                                                "price": product_price,
                                                                                "shippingPrice": delivery_price,
                                                                                "seller": shop_name,
                                                                                "redirectUrl": shop_url}}}
        if offer_has_every_information(offer):
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


def delivery_price(driver):
    shops_list = driver.find_elements(By.CLASS_NAME, 'view-offer-details')
    for shop in enumerate(shops_list):
        try:
            time.sleep(3)
            driver.execute_script(
                "document.getElementsByClassName('view-offer-details')[" + str(shop[0]) + "].style"
                                                                                          ".visibility"
                                                                                          " = "
                                                                                          "'visible';")
            time.sleep(3)
            if shop[0] == 0:
                driver.find_element(By.XPATH, '//*[@id="js_cookie-monster"]/div/div/p/button').click()
                time.sleep(3)
            shop[1].click()
            time.sleep(5)
            # TODO remove time.sleep

            info_div = driver.find_element(By.XPATH, '//*[@id="click"]/div[2]/section/ul/li[' + str(shop[0] + 1)
                                           + ']/div/div[2]/div[2]/div[5]/div/ul/li/ul/li/b')
            text = info_div.text
            string = str(text).replace('\n', '').replace(' zł', '').replace(',', '.')
            delivery_price = float(string)

            delivery_price_list.append(delivery_price)
        except:
            delivery_price = 'None'
            delivery_price_list.append(delivery_price)


def get_page_content(phrase, page_type, page_num=0):
    if page_type is PageType.MAIN:
        url = get_main_ceneo_page_url(phrase)
    elif page_type is PageType.NEXT:
        url = get_next_ceneo_page_url(phrase, page_num)
    else:
        url = get_product_page_url(phrase)

    driver = webdriver.Chrome(chrome_options=set_web_driver_options())
    driver.get(url)

    # if page_type is PageType.PRODUCT:
    #     delivery_price(driver)

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

    main_ceneo_page = get_page_content(search_phrase, PageType.MAIN)
    num_of_pages = get_num_of_pages(main_ceneo_page) + 1

    products = extract_products_from_main_page(main_ceneo_page)

    # if request does not return any product
    if not products:
        return product_offers

    for product in products:
        if product_has_ceneo_offers(product):
            click_hash = get_product_click_hash(product)
            product_page = get_page_content(click_hash, PageType.PRODUCT)
            product_data = extract_data_from_product_page(product_page, search_phrase)
            product_offers += product_data
            if len(product_offers) >= 10:
                return product_offers

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
                if len(product_offers) >= 10:
                    return product_offers

    return product_offers


def get_product(search_phrases, sorting):
    basket = []
    for search_phrase in search_phrases:
        products = get_product_offers(search_phrase)
        basket.append(products)
        # for offer in products:
        #     print(offer)

    if sorting == 0:
        return sort_by_price(basket)
    if sorting == 1:
        return sort_by_shop_num(basket)
