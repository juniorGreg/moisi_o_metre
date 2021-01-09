from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from blog.views import get_main_context

import json
import requests
import os
import re

from .serializers import *
from .email_notifications import *

# Create your views here.



def index(request):
    context = get_main_context("Boutique", "La boutique du MoisiOMètre", "/store")
    return render(request, "store/index.html", context)

def tests(request):
    if not settings.DEBUG:
        raise Http404

    if request.method == "POST":
        notification = request.POST["notification"]
        print(notification)
        order = Order.objects.get(id=1000)
        if notification == "confirm_order":
            EmailNotifications(order).confirm_order()
        elif notification == "package_shipped":
            EmailNotifications(order).shipping()
        elif notification == "package_returned":
            EmailNotifications(order).package_returned()
        elif notification == "order_failed":
            EmailNotifications(order).order_failed()
        elif notification == "order_canceled":
            EmailNotifications(order).order_canceled()
        elif notification == "order_put_hold":
            EmailNotifications(order).order_on_hold()
        elif notification == "order_remove_hold":
            EmailNotifications(order).order_on_hold_removed()

        else:
            print("notification invalid!")

    return render(request, "store/tests.html")

@csrf_exempt
@api_view(['POST'])
def webhook(request):
    data = request.data

    event_type = data["type"]



    if event_type == "package_shipped":
        shipping_notification(data["data"])
    elif event_type == "package_returned":
        package_returned_notification(data["data"])
    elif event_type == "order_failed":
        order_failed_notification(data["data"])
    elif event_type == "order_canceled":
        order_canceled_notification(data["data"])
    elif event_type == "product_synced" or event_type == "product_updated" \
            or event_type == "stock_updated":
        update_store_products(data["data"])

    elif event_type == "order_put_hold":
        order_on_hold_notification(data["data"])
    elif event_type == "order_remove_hold":
        order_on_hold_removed_notification(data["data"])

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
                    p1 = re.compile(" - ([A-Za-z ]*) / ([0-9 xXSML]{1,5})$")
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

@api_view(['POST'])
def shipping_cost(request):

    print(request.data)

    params = request.data;
    params['currency'] = 'CAD'

    if not params['recipient']:
        ip_address = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
        print(ip_address)
        if ip_address == '127.0.0.1':
            ip_address =  "173.176.163.196"



        req_location = requests.get("https://freegeoip.app/json/%s" % ip_address)
        if req_location.status_code == 200:
            location = req_location.json()
            recipient = { "country_code" : location["country_code"],
                          "city": location["city"],
                          "state_code": location["region_code"],
                          "zip": location["zip_code"]}
            params["recipient"] = recipient
        else:
            recipient = { "country_code" : "CA",
                          "city": "Montreal",
                          "state_code": "QC",
                          "zip": "H3G"}
            params["recipient"] = recipient


    print(params)


    req = requests.post(API_PRINTFUL % "shipping/rates", headers=HEADERS, json=params)
    if req.status_code == 200:
        response = req.json()
        return Response(response["result"])

    return Response({'error': 'shipping cost api failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def order(request):
    print(request.data)

    #validation
    for item in request.data["order"]["items"]:
        variant = Variant.objects.get(id=item["sync_variant_id"])
        item["retail_price"] = variant.price

    req_order = requests.post(API_PRINTFUL % "orders/estimate-costs", headers=HEADERS, json=request.data["order"])
    printful_order = {}
    if req_order.status_code == 200:
        printful_order = req_order.json()["result"]
        total_cost =float(printful_order["retail_costs"]["total"]) + float(printful_order["costs"]["shipping"])
        if total_cost == request.data["total_cost"]:
            print("validated total_cost: %s" % total_cost)
            print("received total_cost: %s" % request.data["total_cost"])
            return Response({"error": "validation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print(req_order.text)
        Response({"error": "extimation costs failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if settings.DEBUG:
        printful_order['id'] = 1000
        printful_order['external_id'] = "@1000"
    else:
        return Response({'error': 'not implemented'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    order = Order.objects.create(id=printful_order["id"],
                                 external_id=printful_order["external_id"],
                                 paypal_id=request.data["paypal_id"],
                                 total_cost=float(printful_order["retail_costs"]["total"]),
                                 shipping_cost=float(printful_order["costs"]["shipping"]),
                                 status="draft")
    order.save()
    req_customer = request.data["order"]["recipient"]
    customer = Customer.objects.create(fullname = req_customer["name"],
                                       address= req_customer["address1"],
                                       country_code=req_customer["country_code"],
                                       state_code= req_customer["state_code"],
                                       zip_code=req_customer["zip"],
                                       email = req_customer["email"],
                                       order=order)
    customer.save()
    for req_item in request.data["order"]["items"]:
        variant = Variant.objects.get(id=req_item["sync_variant_id"])
        order_item = OrderItem.objects.create(variant=variant, order=order, quantity=int(req_item["quantity"]))
        order_item.save()

    EmailNotifications(order).confirm_order()
    return Response({"message": "order has been created"})
