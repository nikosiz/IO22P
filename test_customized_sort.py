import unittest


import customized_sort
from test_customized_sort_baskets import basket_price_sort, result_basket_price_sort, basket_shop_sort, \
    result_basket_shop_sort


class TestCustomizedSort(unittest.TestCase):
    def test_sort_by_price(self):
        result = customized_sort.sort_by_price(basket_price_sort)
        self.assertEqual(result, result_basket_price_sort)

    def test_sort_by_shop_num(self):
        result2 = customized_sort.sort_by_shop_num(basket_shop_sort)
        self.assertEqual(result2, result_basket_shop_sort)


if __name__ == '__main__':
    unittest.main()
