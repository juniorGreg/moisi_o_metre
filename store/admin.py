from django.contrib import admin
from django.utils.html import format_html

from .models import *

# Register your models here.
admin.site.register(VariantImage)



class InlineVariant(admin.StackedInline):
    model = Variant
    extra = 0
    readonly_fields = ["id", "variant_id", "external_id", 'name', 'price', 'size', 'color']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "external_id", "name"]
    inlines = [InlineVariant]

    def has_add_permission(self, request):
        return False



class InlineOrderItem(admin.StackedInline):
    model = OrderItem
    extra = 0

    readonly_fields = ["id", "variant", 'quantity', "quantity_shipped"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class InlineCustomer(admin.StackedInline):
    model = Customer
    extra = 0

    readonly_fields = ["fullname", "address", 'country_code', "state_code", 'zip_code']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class InlineShipment(admin.StackedInline):
    model = Shipment
    extra = 0

    readonly_fields = ["id", "carrier", "service", "tracking_number", "tracking_url", "date_created"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["id", 'external_id', "paypal_id", "status", "total_cost", "shipping_cost"]
    inlines = [InlineCustomer, InlineOrderItem, InlineShipment]
    list_display = ("id", "status", "total_cost", "shipping_cost", "date_created", "date_modified")

    def has_add_permission(self, request):
        return False
