import requests
from django.conf import settings

#API
API_PRINTFUL_WEBHOOKS = "https://api.printful.com/webhooks"
HEADERS = {'Authorization': 'Basic %s' % settings.PRINTFUL_API_KEY }
DEBUG_WEBHOOK = "https://moisidev.xyz/store/webhook"
PROD_WEBHOOK = "https://moisi-o-metre.herokuapp.com/store/webhook"

def run():

    current_webhook = PROD_WEBHOOK
    if settings.DEBUG:
        current_webhook = DEBUG_WEBHOOK

    req = requests.get(API_PRINTFUL_WEBHOOKS, headers=HEADERS)
    if req.status_code != 200:
        print("Error get webhooks")
        return

    result = req.json()["result"]

    update_webhooks = True

    if result["url"]:
        update_webhooks = result["url"] != current_webhook

    print(update_webhooks)

    if update_webhooks:
        print("update webhook")
        params = {
            'url': current_webhook,
            'types': [
                'order_remove_hold',
                'order_put_hold',
                'product_updated',
                'product_synced',
                'order_canceled',
                'order_failed',
                'package_returned',
                'package_shipped'
            ]
        }
        req = requests.post(API_PRINTFUL_WEBHOOKS, headers=HEADERS, json=params)
        if req.status_code != 200:
            print(req.json())
            print('Error updated webhooks')
            return

        print(req.json())
