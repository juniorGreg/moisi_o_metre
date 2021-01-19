from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Reference)
admin.site.register(About)
admin.site.register(MediaLink)
admin.site.register(PostStatistics)
class InLineRottentPoint(admin.StackedInline):
    model = RottenPoint
    extra = 1

class MediaLinkInline(admin.TabularInline):
    model = MediaLink

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [InLineRottentPoint]
