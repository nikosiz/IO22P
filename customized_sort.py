# SortType = PRICE
# the cheapest offer for every item (aka search phrase) is added to cart
def sort_by_price(basket):
    output_basket = []
    for item in basket:
        item.sort(key=get_summary_price)
        output_basket.append(item[0])
    return output_basket


# summary price = product_price + delivery_price
def get_summary_price(element):
    return float(float(element['resultProduct']['offer']['price']) + element['resultProduct']['offer']['shippingPrice'])


# SortType = SHOP_NUM
# cart should contain items from the smallest possible number of shops
def sort_by_shop_num(basket):
    output_basket = []
    # sorting by price before removing duplicate shops,
    # in order to choose the cheapest offer in the same shop
    for item in basket:
        item.sort(key=get_summary_price)

    # before checking which shop has the most offers
    # it is necessary to remove duplicate offers
    basket, shops_list = remove_duplicate_shops(basket)

    # counting number of offers per shop
    for shop in shops_list:
        for item in basket:
            if item_is_in_shop(shop[0], item):
                shop[1] += 1

    shops_list = sort_shops(shops_list)

    # adding items to cart, starting from  most popular shop
    for item in basket:
        for shop in shops_list:
            if item_is_in_shop(shop[0], item):
                product_offer = get_product_offer_from_shop_name(shop[0], item)
                output_basket.append(product_offer)
                break
    return output_basket


# sorting shops by number of offers per shop
def sort_shops(shop_list):
    shop_list.sort(reverse=True, key=lambda x: x[1])
    return shop_list


def get_product_offer_from_shop_name(shop, item):
    for item_offer in item:
        if item_offer['resultProduct']['offer']['seller'] == shop:
            return item_offer


def item_is_in_shop(shop, item):
    for item_offer in item:
        if item_offer['resultProduct']['offer']['seller'] == shop:
            return True
    return False


def remove_duplicate_shops(basket):
    basket_without_duplicates = []
    shops_list = []
    for item in basket:
        item_without_duplicates = []
        for item_offer in item:
            if item_offer['resultProduct']['offer']['seller'] not in shops_list:
                shops_list.append([item_offer['resultProduct']['offer']['seller'], 0])
                item_without_duplicates.append(item_offer)
        basket_without_duplicates.append(item_without_duplicates)

    return basket_without_duplicates, shops_list

