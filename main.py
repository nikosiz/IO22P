from scraping import get_product_offers


def main(search_phrase):
    product_offers = get_product_offers(search_phrase)
    return product_offers


products = main('lego minecraft wyspa zombie')
for product in products:
    for info in product:
        print(info, end=' ')
    print()
