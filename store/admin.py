from django.contrib import admin
from django.utils.html import format_html

from .models import *

# Register your models here.
#admin.site.register(Product)
#admin.site.register(Variant)

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

    def has_delete_permission(self, request, obj=None):
        print("papaya")
        return False
