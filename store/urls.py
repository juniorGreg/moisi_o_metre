from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="store_index"),
    path("products", views.products, name="store_products"),
    path("products/<int:start_index>", views.products, name="store_products"),
    path("products/<int:start_index>/<int:length>", views.products, name="store_products"),
    path("webhook", views.webhook, name="store_webhook"),
    path("shipping_cost", views.shipping_cost, name="store_shipping_cost"),
    path("order", views.order, name="order"),
    path("tests/", views.tests, name="tests")

]
