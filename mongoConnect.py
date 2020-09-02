from pymongo import MongoClient
from setting import mongoDB_url_test, mongoDB_url_prod
# pprint library is used to make the output look more pretty
from pprint import pprint


def mongo_connect():
    # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
    client = MongoClient(mongoDB_url_test)
    db = client.newTestingDB
    collection = db.products
    # Issue the serverStatus command and print the results
    products = collection.find()
    for product in products:
        pprint(product)
    return db
