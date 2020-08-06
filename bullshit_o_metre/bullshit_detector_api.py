
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import spacy
from collections import Counter
from langdetect import detect
from .models import *
import asyncio

from multiprocessing import Process, Queue

from pytube import YouTube
from pytube import exceptions

import html

from joblib import load

from django.conf import settings

import re

class TextTooShortException(Exception):

    def __init__(self):
        super().__init__("The text is too short to be evaluate and labeled.")

class YoutubeNoCaptionException(Exception):

    def __init__(self):
        super().__init__("It's a youtube video but there are no captions.")

class EncodingNotFoundException(Exception):

    def __init__(self):
        super().__init__("Encoding not found.")

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

    print(encoding)

    if not encoding:
        raise EncodingNotFoundException()

    return encoding


def retrieve_text_from_website(q, url):
    asyncio.set_event_loop(asyncio.new_event_loop())

    session = HTMLSession()
    r = session.get(url)
    print(r.html)
    r.html.render()

    soup = BeautifulSoup(r.html.html, 'lxml')
    print(soup.original_encoding)



    text = ""
    for tag in soup.find_all("p"):
        text += " "
        text += tag.text

    text = " ".join(text.split())

    title = soup.title.text
    if soup.h1:
        title = soup.h1.text


    if not soup.original_encoding:
        encoding = get_text_encoding(soup)

        text = text.encode(encoding, 'ignore').decode("utf-8", 'ignore')
        title = title.encode(encoding, 'ignore').decode("utf-8", 'ignore')

    if len(text) > 25000:
        text = text[:25000]

    print("len text: ")
    print(len(text))
    print(title)

    q.put(title)
    q.put(text)
    print("okiii2")

def get_captions_text_from_youtube(url, lang_code='fr'):

    try:

        yt = YouTube(url)

        if lang_code in yt.captions:

            caption = yt.captions[lang_code]

            bs = BeautifulSoup(caption.xml_captions, 'lxml')
            texts = ""
            for text in bs.find_all('text'):
                if '[' in text.text:
                    continue
                texts += text.text
                texts += " "
            #print(texts)
            texts = html.unescape(texts)

            if len(texts) > 25000:
                texts = text[:25000]


            print(texts)
            return yt.title, texts, True, False
        else:
            return None, 'no captions', True, True
    except exceptions.RegexMatchError as e:
        return None, "it's not a youtube url", False, True
    except:
        return None, 'no caption', True, True


def get_text_from_website(url):
    queue = Queue()
    p = Process(target= retrieve_text_from_website, args=(queue, url))
    p.daemon = True
    p.start()

    p.join()

    title = queue.get()
    text = queue.get()
    print(title)
    #print(result)

    return title, text

def get_info_from_url(url):
    print(url)
    title, text, is_youtube_url, errors = get_captions_text_from_youtube(url)

    if is_youtube_url and errors:
        raise YoutubeNoCaptionException()

    if not is_youtube_url:
        title, text = get_text_from_website(url)

    if len(text) < 100:
        raise TextTooShortException()

    lang = detect(text)

    return title, text, lang

def add_website(website):

    title, text, lang = get_info_from_url(website['url'])

    return LabeledWebSite.objects.create(title=title, url=website['url'], texts=text, is_bullshit=website['is_bullshit'], lang=lang)

def evaluate_website(url):
    title, text, lang = get_info_from_url(url)

    bsd = load(settings.BASE_DIR+"/bsd.joblib")
    preds = bsd.predict(text)
    print(preds)

    return title, preds[0][1]
