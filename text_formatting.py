def get_main_ceneo_page_url(search_text):
    template = 'https://www.ceneo.pl/Zabawki;szukaj-{};0112-0.htm'
    search_term = search_text.replace(' ', '+')
    return template.format(search_term)


def get_product_page_url(click_hash):
    product_url_template = 'https://www.ceneo.pl{}'
    return product_url_template.format(click_hash)


def get_next_ceneo_page_url(search_text, page_idx):
    template = 'https://www.ceneo.pl/Zabawki;szukaj-{0};0020-30-0-0-{1};0112-0.htm'
    search_term = search_text.replace(' ', '+')
    return template.format(search_term, page_idx)
