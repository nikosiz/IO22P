from scraping import get_product_offers


def main(search_phrase, sorting):
    product_offers = get_product_offers(search_phrase, sorting)
    return product_offers

# sortowanie wg ceny = 1, wg ilości sklepów = 0
products = main('lego minecraft zo', 1)
for product in products:
    for info in product:
        print(info, end=' ')
    print()
