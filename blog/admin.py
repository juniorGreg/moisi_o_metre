from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Reference)
admin.site.register(About)

class InLineRottentPoint(admin.StackedInline):
    model = RottenPoint
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [InLineRottentPoint]
