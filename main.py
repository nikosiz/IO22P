from scraping import get_product


def main(search_phrase, sorting):
    product_offers = get_product(search_phrase, sorting)
    return product_offers


# sortowanie wg ceny = 1, wg ilości sklepów = 0
request = ['tamagotchi niebieskie', 'lalka barbie magia', 'kotek psotek']
products = main(request, 0)

for product in products:
    for info in product:
        print(info, end=' ')
    print()
