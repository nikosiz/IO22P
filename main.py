import json
from flask import Flask, request
from scraping import get_product


def main(search_phrase, sorting):
    product_offers = get_product(search_phrase, sorting)
    return product_offers


app = Flask(__name__)


@app.route('/search')
def search():
    input_data = request.args.getlist('product')
    sorting = int(request.args.get('sorting'))
    basket = main(input_data, sorting)
    response = json.dumps(basket)
    return response


if __name__ == '__main__':
    app.run()
