from mongoConnect import *
from woocommerceConnect import *
from pprint import pprint
from setting import *


def print_sep():
    print('------------------------------------------')


if __name__ == '__main__':

    # connect to test client
    client = mongo_connect(mongoDB_url_test)

    if client is None:
        print_sep()
        print('connect to mongo client failed')
        exit(0)

    # connect test db
    db = client[mongoDB_test_dbname]

    # get collections
    collection_names = db.list_collection_names()

    # check if productcategories collection exist in db
    if 'productcategories' in collection_names:
        categories = db['productcategories'].find().limit(3)
        for category in categories:
            """
            product sample:
            {'_id': '40dcea32-8946-411b-9ebb-6c609602c579', 'parent': None, 'parents': [], 'hasChildren': True, 
            'image': 'acf34aa9-1ca6-4808-990d-ec539d6eaeea', 'level': 1, 'liveStreamCategory': None, 'order': 1, 
            'name': 'Clothing', 'createdAt': datetime.datetime(2020, 6, 16, 22, 45, 44, 626000), '__v': 0}
            """
            if 'assets' in collection_names:
                category_asset = db['assets'].find_one({"_id": category['image']}, {"_id": 1, "url": 1, "type": 1})
                print(category_asset)
    else:
        print_sep()
        print('productcategories not exist')
        exit(0)
