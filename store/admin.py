from django.contrib import admin
from django.utils.html import format_html

from .models import *

# Register your models here.
#admin.site.register(Product)
admin.site.register(Variant)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "external_id", "name"]
