from django import template
from django.contrib.sites.models import Site

register = template.Library()

@register.inclusion_tag("meta_tag.html")
def meta_tag(url, title, description, image=None):
    tag = {"url": 'https://%s%s' % (Site.objects.get_current().domain, url),
            "title": title[0:70], "description": description[:160],
            "image": image.url if image else image }
    return {"tag": tag}
