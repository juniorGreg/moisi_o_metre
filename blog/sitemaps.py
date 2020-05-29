from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse


class PostSitmap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol="https"

    def items(self):
        return Post.objects.order_by('-date_created')[:5]

    def lastmod(self, obj):
        return obj.date_modified

    def location(self, obj):
        return reverse("post", kwargs={"id": str(obj.id)})
