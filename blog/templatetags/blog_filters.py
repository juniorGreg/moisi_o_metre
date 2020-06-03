from django import template
import urllib.parse

register = template.Library()


@register.filter(name="post_urlencode")
def post_urlencode(value):    
    encode_url = urllib.parse.quote(value)
    return encode_url

@register.simple_tag(name="post_share_url_twitter")
def post_share_url_twitter(url, post_id, text):
    complete_url = url + str(post_id)
    encode_url = urllib.parse.quote(complete_url)
    encode_text = urllib.parse.quote(text)
    share_url = "https://twitter.com/intent/tweet?url={}&text={}&hashtags=espritcritique,zététique,humour".format(encode_url, encode_text)
    return share_url
