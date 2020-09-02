from pymongo import MongoClient, errors
# pprint library is used to make the output look more pretty
from pprint import pprint


def mongo_connect(url):
    """
    Connect to mongo atlas
    :return: mongo client
    """
    try:
        # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
        client = MongoClient(url)
        return client
    except errors.ServerSelectionTimeoutError as err:
        print(err)
        return None
    except Exception as e:
        print(e)
        return None
