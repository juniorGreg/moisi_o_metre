
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import spacy
from collections import Counter
from langdetect import detect
from .models import *
import asyncio

from multiprocessing import Process, Queue

from pytube import YouTube
from pytube import exceptions

import html

class TextTooShortException(Exception):

    def __init__(self):
        super().__init__("The text is too short to be evaluate and labeled.")

class YoutubeNoCaptionException(Exception):

    def __init__(self):
        super().__init__("It's a youtube video but there are no captions.")



def retrieve_text_from_website(q, url):
    asyncio.set_event_loop(asyncio.new_event_loop())

    session = HTMLSession()
    r = session.get(url)
    print(r.html)
    r.html.render()
    print("render done")


    soup = BeautifulSoup(r.html.html, 'lxml')
    #print(soup.find_all('p')[0].text)

    text = ""
    for tag in soup.find_all("p"):
        text += " "
        text += tag.text

    text = " ".join(text.split())
    title = soup.h1.text


    if len(text) > 25000:
        text = text[:25000]

    print("len text: ")
    print(len(text))

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
    print(title)

    return title, 0.0
