import re


# main function in this module, called by scrap_product_offers() in scraping module
# given product page, extracts offers data and returns ready offers
def extract_data_from_product_page(product_page, search_phrase):
    data = []

    product_name = get_product_name(product_page).replace('\n', '')
    thumbnail_url = get_thumbnail_url(product_page)

    shop_offers = get_shop_offers_from_product_page(product_page)
    for shop_offer in shop_offers:
        shop_name = get_shop_name(shop_offer)
        product_price = get_product_price(shop_offer)
        delivery_price = get_delivery_price(shop_offer, product_price)
        shop_url = get_shop_url(shop_offer)
        offer = {'searchProduct': search_phrase,
                 "resultProduct": {"name": product_name,
                                   "thumbnailUrl": thumbnail_url,
                                   "offer": {"price": product_price, "shippingPrice": delivery_price,
                                             "seller": shop_name, "redirectUrl": shop_url}}}
        if offer_has_every_information(offer):
            data.append(offer)

    return data


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


def get_delivery_price(shop_offer, product_price):
    try:
        delivery_price_info = shop_offer.find(class_='product-delivery-info js_deliveryInfo')
        delivery_price_text = delivery_price_info.text
        if delivery_price_text == '\nDarmowa wysyłka\n':
            return 0.0
        elif delivery_price_text == '\nszczegóły dostawy\n':
            return 0.0
        else:
            delivery_price_text = str(delivery_price_text).replace(',', '.')
            summary_price = re.findall(r"[-+]?(?:\d*\.*\d+)", delivery_price_text)[0]
            delivery_price = float(summary_price) - float(product_price)
            try:
                delivery_price = round(delivery_price, 2)
            except:
                pass
            return delivery_price
    except:
        return 'None'


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


def get_shop_offers_from_product_page(product_page):
    return product_page.find_all(class_='product-offers__list__item js_productOfferGroupItem')
