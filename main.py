from mongoConnect import *
from woocommerceConnect import *
from pprint import pprint
from setting import *

if __name__ == '__main__':

    # connect to test client
    client = mongo_connect(mongoDB_url_test)

    # connect test db
    db = client[mongoDB_test_dbname]

    # get collections
    collection_names = db.list_collection_names()
    # check if assets collection exist in db
    asset_urls = []
    if 'assets' in collection_names:
        assets = db['assets'].find().limit(5)
        for asset in assets:
            print(asset)
    # check if productcategories collection exist in db
    if 'productcategories' in collection_names:
        categories = db['productcategories'].find()
        for category in categories:
            print(category)
            exit(0)

