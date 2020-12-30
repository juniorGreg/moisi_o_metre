from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.views import get_main_context

import json
import requests
import os
import re




from .serializers import *

# Create your views here.



def index(request):
    context = get_main_context("Boutique", "La boutique du MoisiOMètre", "/store")
    return render(request, "store/index.html", context)

@csrf_exempt
@require_POST
def webhook(request):
    data = json.loads(request.body.decode("utf-8"))

    event_type = data["type"]



    if event_type == "package_shipped":
        print("package shipped")
    elif event_type == "package_returned":
        print("package returned")
    elif event_type == "order_failed":
        print("order failed")
    elif event_type == "order_canceled":
        print("order canceled")
    elif event_type == "product_synced" or event_type == "product_updated" \
            or event_type == "stock_updated":
        update_store_products(data["data"])

    elif event_type == "order_put_hold":
        print("order put hold")
    elif event_type == "order_remove_hold":
        print("order remove holf")
    else:
        print("event type unknown")
        print(event_type)

    return HttpResponse("success")



#API
API_PRINTFUL = "https://api.printful.com/%s"
HEADERS = {'Authorization': 'Basic %s' % settings.PRINTFUL_API_KEY }

def upload_image_to_model(image, url):
    req_img = requests.get(url, stream=True)

    if req_img.status_code == 200:
        tmp_file = NamedTemporaryFile(delete=True)
        file_name = os.path.basename(url)
        tmp_file.write(req_img.raw.read())
        tmp_file.flush()

        image.save(file_name, File(tmp_file), save=True)

        tmp_file.close()


def update_store_products(new_data):
    #print(new_data)
    params = {
        "status": 'synced'
    }
    r = requests.get(API_PRINTFUL % "sync/products", headers=HEADERS, params=params)


    if r.status_code == 200:

        data = r.json()

        for product in data["result"]:
            reg_product, created = Product.objects.get_or_create(id = product["id"])

            reg_product.name = product["name"]

            if created :
                reg_product.external_id = product["external_id"]

                upload_image_to_model(reg_product.image, product["thumbnail_url"])


            reg_product.save()

            #get variants
            req_variants = requests.get(API_PRINTFUL % "sync/products/%s" % reg_product.id, headers=HEADERS)

            if req_variants.status_code == 200:
                response_req_variants = req_variants.json()
                sync_variants = response_req_variants["result"]["sync_variants"]



                for variant in sync_variants:

                    reg_variant, created = Variant.objects.get_or_create(id = variant["id"])
                    reg_variant.name = variant["name"]
                    reg_variant.price = variant["retail_price"]
                    reg_variant.product = reg_product

                    #Parse color and size of the variant by the name
                    p1 = re.compile(" - ([A-Za-z ]*) / ([0-9 XSML]{1,3})$")
                    m1 = p1.search(reg_variant.name)

                    p2 = re.compile(" - ([A-Za-z ]*)$")
                    m2 = p2.search(reg_variant.name)

                    if m1:
                        reg_variant.color = m1.group(1).lower()
                        reg_variant.size = m1.group(2)
                    elif m2:
                        reg_variant.color = m2.group(1).lower()

                    if created:

                        reg_variant.variant_id = variant["variant_id"]
                        reg_variant.external_id = variant["external_id"]

                        #Parse color and size of the variant by the name
                        p = re.compile(" - ([A-Za-z ]*) / ([0-9 XSML]{1,3})$")

                        m = p.search(reg_variant.name)

                        if m:
                            reg_variant.color = m.group(1).lower()
                            reg_variant.size = m.group(2)
                        else:
                            reg_variant.color = "undefined"
                            reg_variant.size = 'N'

                        files = variant["files"]

                        for file in files:
                            if file["type"] == "preview":
                                upload_image_to_model(reg_variant.thumbnail, file["thumbnail_url"])
                                upload_image_to_model(reg_variant.preview, file["preview_url"])
                                break

                    reg_variant.save()

    print("update_ products")

@api_view(['GET'])
def products(request):
    products = Product.objects.all()

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)
