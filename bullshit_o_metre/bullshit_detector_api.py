
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

from .bullshit_detector import BullshitDetector

bsd = BullshitDetector()
bsd.load_model(settings.BASE_DIR+"/model.json")

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

    print(encoding)

    if not encoding:
        raise EncodingNotFoundException()

    return encoding


def retrieve_text_from_website(q,eq, url):
    asyncio.set_event_loop(asyncio.new_event_loop())

    session = HTMLSession()

    try:
        r = session.get(url)
        r.html.render()

    except Exception as e:
        eq.put(str(e))
        return
    #print(r.html)

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

    yt = YouTube(url)

    if lang_code in yt.captions:

        caption = yt.captions[lang_code]

        #print(yt.captions.keys())

        bs = BeautifulSoup(caption.xml_captions, 'lxml')
        texts = ""
        for text in bs.find_all('text'):
            if '[' in text.text:
                continue
            texts += text.text
            texts += " "

        texts = html.unescape(texts)


        if len(texts) > 25000:
            texts = texts[:25000]


        #print(texts)
        return yt.title, texts
    else:
        raise YoutubeNoCaptionException()
    #except exceptions.RegexMatchError as e:
    #    return None, "it's not a youtube url", False, True



def get_text_from_website(url):
    queue = Queue()
    error_queue = Queue()

    p = Process(target= retrieve_text_from_website, args=(queue, error_queue, url))
    p.daemon = True
    p.start()

    p.join()

    if not error_queue.empty():
        #print(error_queue.get())
        raise Exception(error_queue.get())

    title = queue.get()
    text = queue.get()
    print(title)
    #print(result)

    return title, text

def get_info_from_url(url):
    print(url)
    not_youtube_url = False
    try:
        title, text = get_captions_text_from_youtube(url)
    except exceptions.RegexMatchError:
        print("Not a youtube url")
        not_youtube_url = True

    if not_youtube_url:
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

    if lang != "fr":
        raise InvalidLanguage()


    preds = bsd.predict(text)
    print(preds)

    return title, int(preds[0][1] * 100)
