from mongoConnect import *
from woocommerceConnect import *
from pprint import pprint
from setting import *

if __name__ == '__main__':
    client = mongo_connect(mongoDB_url_test)
    db = mongo_get_db(client, 'aaa')
