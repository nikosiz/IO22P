from scraping import get_product


def main(search_phrase, sorting):
    product_offers = get_product(search_phrase, sorting)
    return product_offers


# sortowanie wg ceny = 1, wg ilości sklepów = 0
request = ['vfsdagag']
basket = main(request, 1)

print('\nOstatecznie koszyk wyglada tak\n')
for item in basket:
    print(item)
