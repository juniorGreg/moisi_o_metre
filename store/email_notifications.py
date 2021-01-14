from django.core.mail import send_mail
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

import requests

from .models import *

import os


class EmailNotifications:
    def __init__(self, order):
        self.order = order

        self.email_address = order.customer_set.all()[0].email

    def confirm_order(self):
        msg = {
            "subject": "Confirmation de commande",
            "message": "votre commande est confirmée. D'ici une semaine votre commande devrait être expédiée."
        }

        self._send_mail_notification(msg)

    def shipping(self):
        msg = {
            "subject": "Livraison de commande",
            "message": "votre commande a été expédiée. Les détails sont ci-bas."
        }

        self._send_mail_notification(msg)

    def package_returned(self):
        msg = {
            "subject": "Commande retournée",
            "message": "votre commande a été retournée."
        }

        self._send_mail_notification(msg)

    def order_failed(self):
        msg = {
            "subject": "Votre commande a échouée",
            "message": "votre commande a échouée."
        }

        self._send_mail_notification(msg)

    def order_canceled(self):
        msg = {
            "subject": "Commande annulée",
            "message": "votre commande a annulée."
        }

        self._send_mail_notification(msg, admin_only=True)

    def order_on_hold(self):
        msg = {
            "subject": "Commande en attente",
            "message": "votre commande a été mis en attente."
        }

        self._send_mail_notification(msg, admin_only=True)

    def order_on_hold_removed(self):
        msg = {
            "subject": "Commande plus en attente",
            "message": "votre commande n'est plus en attente."
        }

        self._send_mail_notification(msg, admin_only=True)




    def _send_mail_notification(self, msg, admin_only=False):

        shipped_items = OrderItem.objects.filter(order=self.order, quantity_shipped__gt=0)
        print(shipped_items)

        context = {'msg': msg, 'order': self.order, 'shipped_items': shipped_items }

        html_content = render_to_string('store/email_notification.html', context=context).strip()

        if admin_only:
            to = [settings.EMAIL_ADMIN]
        else:
            to = [settings.EMAIL_ADMIN, self.email_address]

        email = EmailMultiAlternatives(msg["subject"], html_content, settings.DEFAULT_FROM_EMAIL, to)

        email.mixed_subtype = "related"
        email.attach_alternative(html_content, "text/html")

        req_image = requests.get("https://moisi-bucket.s3.us-east-2.amazonaws.com/images/moisiometre_email.gif", stream=True)
        if req_image.status_code == 200:
            image = MIMEImage(req_image.raw.read(), "gif")
            image.add_header('Content-ID', '<moisiometre_email.gif>')
            image.add_header("Content-Disposition", "inline", filename="moisiometre_email.gif")
            email.attach(image)

        email.send()


def _get_and_update_order(data):
    printful_order = data["order"]
    if settings.DEBUG:
        order = Order.objects.get(id='1000')
    else:
        order = Order.objects.get(id= printful_order["id"])
    order.status = printful_order["status"]
    order.save()
    return order

def _update_order_items(data, db_order):
    shipment_items = data["shipment"]["items"]
    order_items = data["order"]["items"]
    #print(order_items)
    try:
        order_items_by_id = { order_item["id"] : order_item["sync_variant_id"] for order_item in order_items}
    except KeyError as e:
        print(e)
        return

    #print(order_items_by_id)
    #print(shipment_items)

    for shipment_item in shipment_items:
        if shipment_item["item_id"] in order_items_by_id:
            sync_variant_id = order_items_by_id[shipment_item["item_id"]]
            db_variant = Variant.objects.filter(id = sync_variant_id).first()
            if db_variant is not None:
                db_order_item = OrderItem.objects.filter(order = db_order, variant=db_variant).first()
                if db_order_item is not None:
                    db_order_item.quantity_shipped = shipment_item["quantity"]
                    db_order_item.save()





def shipping_notification(data):

    printful_shipment = data["shipment"]
    print(printful_shipment)

    order = _get_and_update_order(data)
    shipment, created = Shipment.objects.get_or_create(id=printful_shipment["id"])

    shipment.carrier = printful_shipment["carrier"]
    shipment.service = printful_shipment["service"]
    shipment.tracking_number = printful_shipment["tracking_number"]
    shipment.tracking_url = printful_shipment["tracking_url"]
    shipment.order = order

    shipment.save()
    _update_order_items(data, order)

    #update order items


    EmailNotifications(order).shipping()


def package_returned_notification(data):
    order = _get_and_update_order(data)
    EmailNotifications(order).package_returned()

def order_failed_notification(data):
    order = _get_and_update_order(data)
    EmailNotifications(order).order_failed()

def order_canceled_notification(data):
    order = _get_and_update_order(data)
    EmailNotifications(order).order_canceled()

def order_on_hold_notification(data):
    order = _get_and_update_order(data)
    EmailNotifications(order).order_on_hold()

def order_on_hold_removed_notification(data):
    order = _get_and_update_order(data)
    EmailNotifications(order).order_on_hold_removed()
