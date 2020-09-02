from mongoConnect import *
from woocommerceConnect import *
from pprint import pprint
from setting import *

if __name__ == '__main__':
    client = mongo_connect(mongoDB_url_test)
    db = mongo_get_db(client, mongoDB_test_dbname)
    collection_names = db.list_collection_names()
    for collection_name in collection_names:
        print(collection_name)
