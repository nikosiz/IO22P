
def get_summary_price(element):
    return float(element['Price']) + element['Delivery Price']


def sort_by_price(basket):
    output_basket = []
    for item in basket:
        item.sort(key=get_summary_price)
        output_basket.append(item[0])
    return output_basket


def sort_by_shop_num(basket):
    pass
