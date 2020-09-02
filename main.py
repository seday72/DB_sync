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

    # loop collections
    print(collection_names)

