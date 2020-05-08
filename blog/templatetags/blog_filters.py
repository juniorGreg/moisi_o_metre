from django import template
import urllib.parse

register = template.Library()


@register.filter(name="post_urlencode")
def post_urlencode(value, arg):
    complete_url = value + str(arg)
    encode_url = urllib.parse.quote(complete_url)
    print(complete_url)
    print(encode_url)
    return encode_url
