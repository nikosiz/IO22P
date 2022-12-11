def get_main_ceneo_page_url(search_text):
    template = 'https://www.ceneo.pl/Zabawki;szukaj-{}'
    search_term = search_text.replace(' ', '+')
    return template.format(search_term)


def get_product_page_url(click_hash):
    product_url_template = 'https://www.ceneo.pl{}'
    return product_url_template.format(click_hash)
