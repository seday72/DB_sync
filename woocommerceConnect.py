from woocommerce import API
from setting import woocommerce_ck, woocommerce_url, woocommerce_cs


def woocommerce_connect():
    wcapi = API(
        url=woocommerce_url,
        consumer_key=woocommerce_ck,
        consumer_secret=woocommerce_cs,
        version="wc/v3"
    )
    return wcapi


def get_categories(wcapi):
    try:
        result = wcapi.get('products/categories')
        if result.status_code == 200:
            return result.json()
        else:
            return None
    except:
        return None


def woocommerce_add_category(wcapi, data):
    try:
        r = wcapi.post('products/categories', data)
        if r.status_code == 201:
            return r.json()['id']
        elif r.status_code == 400:
            if r.json()['code'] == 'woocommerce_rest_invalid_remote_image_url':
                return -1 # remote image url invalid error
            return r.json()['data']['resource_id']
        else:
            print(r.json())
            return 0
    except Exception as e:
        print('error {}, {}'.format(e, data))
        return 0

