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
        self.static_url = settings.STATIC_URL
        if self.static_url == "/static/":
            self.static_url =  "http://localhost:8000"+self.static_url

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

        context = {'msg': msg, 'order': self.order }

        html_content = render_to_string('store/email_notification.html', context=context).strip()

        if admin_only:
            to = [settings.EMAIL_ADMIN]
        else:
            to = [settings.EMAIL_ADMIN, self.email_address]

        email = EmailMultiAlternatives(msg["subject"], html_content, settings.DEFAULT_FROM_EMAIL, to)

        email.mixed_subtype = "related"
        email.attach_alternative(html_content, "text/html")

        req_image = requests.get(self.static_url+"images/moisiometre_email.gif", stream=True)

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


def shipping_notification(data):
    print(data)
    printful_shipment = data["shipment"]

    order = _get_and_update_order(data)
    shipment = Shipment.objects.create(id=printful_shipment["id"],
                               carrier=printful_shipment["carrier"],
                               service=printful_shipment["service"],
                               tracking_number=printful_shipment["tracking_number"],
                               tracking_url=printful_shipment["tracking_url"],
                               order=order)

    shipment.save()

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
