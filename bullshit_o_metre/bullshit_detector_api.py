
import requests
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import spacy
from collections import Counter
from langdetect import detect
from .models import *
import asyncio


from pytube import YouTube
from pytube import exceptions

import html

from joblib import load

from django.conf import settings

import re

from moisi_o_metre.wsgi import bsd

MAX_TEXT_LENGTH = 25000

http_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}


class TextTooShortException(Exception):

    def __init__(self):
        super().__init__("The text is too short to be evaluate and labeled.")

class YoutubeNoCaptionException(Exception):

    def __init__(self):
        super().__init__("It's a youtube video but there are no captions.")

class EncodingNotFoundException(Exception):

    def __init__(self):
        super().__init__("Encoding not found.")

class InvalidLanguage(Exception):

    def __init__(self):
        super().__init__("Language invalid.")

def get_text_encoding(soup):
    encoding = None

    for meta in soup.find_all("meta"):
        if "charset" in meta.attrs.keys():
            encoding = meta["charset"]

    if not encoding:
        meta = soup.find("meta", attrs={"http-equiv": re.compile("(?i)Content-Type")})
        if meta:
            if "content" in meta.attrs.keys():
                encoding = meta["content"].replace("text/html; charset=", "").lower()

    #print(encoding)

    if not encoding:
        raise EncodingNotFoundException()

    return encoding


def retrieve_text_from_website(url):


    r= requests.get(url, headers=http_headers)


    soup = BeautifulSoup(r.text, 'lxml')

    text = "".join([tag.text for tag in soup.find_all("p")])

    text = " ".join(text.split())

    title = soup.title.text
    if soup.h1:
        title = soup.h1.text


    if not soup.original_encoding:
        encoding = get_text_encoding(soup)

        text = text.encode(encoding, 'ignore').decode("utf-8", 'ignore')
        title = title.encode(encoding, 'ignore').decode("utf-8", 'ignore')

    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]

    #print("len text: ")
    #print(len(text))
    #print(title)

    return title, text


def get_captions_text_from_youtube(url, lang_code='fr'):

    yt = YouTube(url)

    if lang_code in yt.captions:

        caption = yt.captions[lang_code]

        #print(yt.captions.keys())

        soup = BeautifulSoup(caption.xml_captions, 'lxml')
        text = " ".join([tag.text for tag in soup.find_all('text') if '[' not in tag.text])

        text = html.unescape(text)


        if len(text) > MAX_TEXT_LENGTH:
            text = text[:MAX_TEXT_LENGTH]


        #print(texts)
        return yt.title, text
    else:
        raise YoutubeNoCaptionException()
    #except exceptions.RegexMatchError as e:
    #    return None, "it's not a youtube url", False, True

def get_info_from_url(url):
    #print(url)
    not_youtube_url = False
    try:
        title, text = get_captions_text_from_youtube(url)
    except exceptions.RegexMatchError:
        print("Not a youtube url")
        not_youtube_url = True

    if not_youtube_url:
        title, text = retrieve_text_from_website(url)


    if len(text) < 100:
        raise TextTooShortException()

    lang = detect(text)

    return title, text, lang

def add_website(website):

    title, text, lang = get_info_from_url(website['url'])

    return LabeledWebSite.objects.create(title=title, url=website['url'], texts=text, is_bullshit=website['is_bullshit'], lang=lang)

def evaluate_website(url):
    title, text, lang = get_info_from_url(url)

    if lang != "fr":
        raise InvalidLanguage()


    preds = bsd.predict(text)
    print(preds)

    return title, int(preds[0][1] * 100)
