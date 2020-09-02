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
