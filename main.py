from mongoConnect import *
from woocommerceConnect import *
from pprint import pprint
from setting import *


def print_sep():
    print('------------------------------------------')


if __name__ == '__main__':
    # connect to woocommerce api
    woo_api = woocommerce_connect()

    # get woocommerce categories
    woo_categories = get_categories(woo_api)
    # pprint(woo_categories)

    # connect to test client
    client = mongo_connect(mongoDB_url_prod)
    # client = mongo_connect(mongoDB_url_test)
    if client is None:
        print_sep()
        print('connect to mongo client failed')
        exit(0)

    print_sep()
    print('MongoDB Connection Success')

    # connect test db
    db = client[mongoDB_prod_dbname]
    # db = client[mongoDB_test_dbname]

    # get collections
    collection_names = db.list_collection_names()

    # check if productcategories collection exist in db
    mongo_categories = []
    if 'productcategories' in collection_names:
        categories = db['productcategories'].find().sort('level')
        for category in categories:
            print_sep()
            """
            product sample:
            {'_id': '40dcea32-8946-411b-9ebb-6c609602c579', 'parent': None, 'parents': [], 'hasChildren': True, 
            'image': 'acf34aa9-1ca6-4808-990d-ec539d6eaeea', 'level': 1, 'liveStreamCategory': None, 'order': 1, 
            'name': 'Clothing', 'createdAt': datetime.datetime(2020, 6, 16, 22, 45, 44, 626000), '__v': 0}
            """
            print('category in mongo: {}, {}'.format(category['name'], category['level']))
            m_category = {
                'id': category['_id'],
                'level': category['level'],
                'name': category['name'],
                'asset': None
            }
            cat_data = {
                'name': category['name'],
            }
            if 'assets' in collection_names:
                category_asset = db['assets'].find_one({"_id": category['image']}, {"_id": 1, "url": 1, "type": 1})
                # print(category_asset)
                if category_asset:
                    # print('category image url: {}'.format(category_asset['url']))
                    m_category['asset'] = category_asset
                    cat_data['image'] = {'src': category_asset['url']}
            if category['level'] != 1:
                for p_category in mongo_categories:
                    if p_category['id'] == category['parent']:
                        cat_data['parent'] = p_category['woo_id']
                        break
            woo_id = woocommerce_add_category(woo_api, cat_data)
            if woo_id == -1:
                cat_data_without_image = {'name': category['name']}
                if 'parent' in cat_data:
                    cat_data_without_image['parent'] = cat_data['parent']
                woo_id = woocommerce_add_category(woo_api, cat_data_without_image)
            if woo_id == 0:
                print('insert category to woocommerce failed!')
                continue
            m_category['woo_id'] = woo_id

            print('category in woocommerce: {}'.format(woo_id))

            # get products of current category
            mongo_products = db['products'].find({"category": category['_id'], 'isDeleted': False})

            # loop category products
            for product in mongo_products:
                product_data = {
                    'name': product['title'],
                    'type': 'simple',
                    'price': "%s" % product['oldPrice'],
                    'regular_price': "%s" % product['price'],
                    'description': product['description'],
                    'short_description': product['description'],
                    'categories': [{'id': woo_id}]
                }
                # get product images
                product_assets = []
                if product and 'assets' in product:
                    for p_asset in product['assets']:
                        asset = db['assets'].find_one({"_id": p_asset}, {"_id": 1, "url": 1, "type": 1})
                        product_assets.append({'src': asset['url']})
                if product_assets:
                    product_data['images'] = product_assets
                mongo_brand = db['brands'].find_one({'_id': product['brand']})

                # pprint(product_assets)

                # get brand from mongo db and insert to woocommerce tag
                if mongo_brand and 'name' in mongo_brand:
                    tag_data = {'name': mongo_brand['name']}
                    tag_id = woocommerce_add_tag(woo_api, tag_data)
                    if tag_id != 0:
                        product_data['tags'] = []
                        product_data['tags'].append({'id': tag_id})

                product_id = woocommerce_product_add(woo_api, product_data, False)

                print_sep()
                print("insert product {}". format(product_id))
            mongo_categories.append(m_category)
        pprint(mongo_categories)
    else:
        print_sep()
        print('productcategories not exist')
        exit(0)
