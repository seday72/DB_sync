from mongoConnect import *
from woocommerceConnect import *
from pprint import pprint

if __name__ == '__main__':
    woo_api = woocommerce_connect()
    try:
        woo_products = woo_api.get('products')
        if woo_products.status_code == 200:
            pprint(woo_products.json())
    except:
        print('Error')
    # mongo_connect()
