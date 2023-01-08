from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

from text_formatting import *


class PageType:
    MAIN = 0
    PRODUCT = 1
    NEXT = 2


delivery_price_list = []
sorted_list = []


def set_web_driver_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless=chrome')  # without opening browser window
    options.add_argument('no-sandbox')
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
        info_div = shop_offer.find(class_='product-offer__product__offer-details__name')
        info = info_div.find('a').get('href')
    except:
        info = 'None'
    return info


def extract_data_from_product_page(product_page):
    # TODO error handling
    data = []
    product_name = get_product_name(product_page).replace('\n', '')

    shop_offers = get_shop_offers_from_product_page(product_page)
    for shop_offer in shop_offers:
        shop_name = get_shop_name(shop_offer)
        product_price = get_product_price(shop_offer)
        delivery_price = get_delivery_price()
        shop_url = get_shop_url(shop_offer)
        offer = [product_name, shop_name, product_price, delivery_price, shop_url]
        data.append(offer)

    return data


def get_product_click_hash(product):
    return product.find('a').get('href')


def extract_products_from_main_page(page):
    return page.find_all(class_='cat-prod-row__body')


# chyba to nie będzie potrzebne jeśli sortowanie będzie działać dobrze
def get_num_of_pages(main_ceneo_page):
    products_per_page = 30
    sidebar_nav = main_ceneo_page.find(class_='grid-cat__site js_sidebar')
    quantity = sidebar_nav.find(class_='cat-nav__title__quantity').getText()
    num_of_all_products = int(quantity)
    num_of_pages = num_of_all_products // products_per_page
    return num_of_pages


def shop_sorting(driver):
    global sorted_list
    sorting_list = driver.find_elements(By.CLASS_NAME, 'cat-prod-row')
    # nie wiem czemu pętla idzie tylko do przedostatniego elementu i nie uwzględnia ostatniego
    for product in enumerate(sorting_list):
        try:
            info = driver.find_element(By.XPATH, '//*[@id="body"]/div/div/div[3]/div/section/div[2]/div['
                                       + str(product[0] + 1) + ']/div/div[2]/div[2]/a[2]/span')
            string = str(info.text)

            div = driver.find_element(By.XPATH, '//*[@id="body"]/div/div/div[3]/div/section/div[2]/div['
                                      + str(product[0] + 1) + ']/div/div[1]/a')
            href = div.get_property('href').replace('https://www.ceneo.pl', '')

            if string == '':
                list1 = [1, href]
            else:
                num = re.findall(r'\b\d+\b', string)[0]
                list1 = [int(num), href]
            sorted_list.append(list1)
            sorted_list = sorted(sorted_list, key=lambda x: x[0], reverse=True)
        except:
            pass


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
            delivery_price = 0.0
            delivery_price_list.append(delivery_price)


def get_page_content(phrase, page_type, sorting, page_num=0):
    global sorted_list
    if page_type is PageType.MAIN:
        url = get_main_ceneo_page_url(phrase)
    elif page_type is PageType.NEXT:
        url = get_next_ceneo_page_url(phrase, page_num)
    else:
        url = get_product_page_url(phrase)

    driver = webdriver.Chrome(chrome_options=set_web_driver_options())
    driver.get(url)

    # sortowanie po cenie
    if page_type is PageType.MAIN and sorting == 1:
        driver.find_element(By.XPATH, '//*[@id="body"]/div/div/div[3]/div/section/div[1]/div[2]/div/a/b').click()
        driver.find_element(By.XPATH, '//*[@id="body"]/div/div/div[3]/div/section/div[1]/div[2]/div/div/a[2]').click()
    elif page_type is PageType.MAIN and sorting == 0:
        # sortowanie po sklepach jeśli więcej niż 1 strona
        try:
            num_of_pages = driver.find_element(By.ID, 'page-counter').get_attribute('data-pagecount')
            num_of_pages = int(num_of_pages)
            for page in range(num_of_pages):
                shop_sorting(driver)
                if page < num_of_pages - 1:
                    driver.find_element(By.XPATH, '//*[@id="body"]/div/div/div[3]/div/section/div[1]/div[3]/div[2]/a').click()
            del sorted_list[10:len(sorted_list)]
        # sortowanie po sklepach jeśli tylko 1 strona
        except:
            shop_sorting(driver)
            del sorted_list[10:len(sorted_list)]
    else:
        pass

    if page_type is PageType.PRODUCT:
        delivery_price(driver)
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


def get_product_offers(search_phrase, sorting):
    product_offers = []

    main_ceneo_page = get_page_content(search_phrase, PageType.MAIN, sorting)
    num_of_pages = get_num_of_pages(main_ceneo_page) + 1

    products = extract_products_from_main_page(main_ceneo_page)

    # TODO 10 produktów po cenie i filtry
    for product in products:
        if product_has_ceneo_offers(product):
            click_hash = get_product_click_hash(product)
            if sorting == 0:
                # tu jest błąd bo patrz linijka 116 XD
                product_page = get_page_content(sorted_list[0][1], PageType.PRODUCT, 2)
                sorted_list.pop(0)
            else:
                product_page = get_page_content(click_hash, PageType.PRODUCT, 2)
            product_data = extract_data_from_product_page(product_page)
            product_offers += product_data

    # if there is more than one page, repeat
    for i in range(1, num_of_pages, 1):
        next_ceneo_page = get_page_content(search_phrase, PageType.NEXT, i)

        next_products = extract_products_from_main_page(next_ceneo_page)
        for product in next_products:
            if product_has_ceneo_offers(product):
                click_hash = get_product_click_hash(product)
                product_page = get_page_content(click_hash, PageType.PRODUCT, 2)
                product_data = extract_data_from_product_page(product_page)
                product_offers += product_data

    return product_offers
