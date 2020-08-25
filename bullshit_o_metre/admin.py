from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(LabeledWebSite)
class LabeledWebSiteAdmin(admin.ModelAdmin):
    list_display = ("title", 'is_bullshit')
