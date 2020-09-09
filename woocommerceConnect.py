from woocommerce import API
from setting import woocommerce_ck, woocommerce_url, woocommerce_cs
import traceback


def woocommerce_connect():
    wcapi = API(
        url=woocommerce_url,
        consumer_key=woocommerce_ck,
        consumer_secret=woocommerce_cs,
        version="wc/v3",
        timeout=300
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
                return -1  # remote image url invalid error
            return r.json()['data']['resource_id']
        else:
            print(r.json())
            return 0
    except Exception as e:
        print('error {}, {}'.format(e, data))
        return 0


def woocommerce_add_tag(wcapi, data):
    try:
        r = wcapi.post('products/tags', data)
        if r.status_code == 201:
            return r.json()['id']
        elif r.status_code == 400:
            return r.json()['data']['resource_id']
        else:
            return 0
    except:
        traceback.print_exc()


def woocommerce_product_add(wcapi, product, update=False):
    try:
        r = wcapi.post('products', product)

        print(r.json())
        if r.status_code == 201:
            ret = r.json()['id']
            return ret
        elif r.status_code == 400:
            pid = r.json()['data']['resource_id']
            if update:
                pid = woocommerce_product_update(pid, product)
            return pid
    except:
        traceback.print_exc()

    return 0  # product insert failed


def woocommerce_product_update(wcapi, pid, product):
    try:
        r = wcapi.get('products/%d' % pid)
        if 'images' in r.json():
            for image_attr in r.json()['images']:
                if 'id' in image_attr:
                    product['images'] = [{'id': image_attr['id']}]
                    break

        r = wcapi.put('products/%d' % pid, product)
        if r.status_code == 200:
            return pid  # update success
        else:
            return -1  # update failed
    except:
        traceback.print_exc()
    return -1

