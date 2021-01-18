
import requests
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit

from collections import Counter
from langdetect import detect
from .models import *


import html

from django.conf import settings
from youtube_transcript_api import YouTubeTranscriptApi

import re

from functools import reduce


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

    video_id_re = re.compile("^https?:\/\/([w]{3}\.)?youtube\.com\/watch\?v=(.*)$")
    short_url_video_id_re = re.compile("^https?:\/\/y(.{2,4}).be\/(.*)$")
    video_match = video_id_re.search(url)

    video_id = ""

    if video_match:
        video_id = video_match.group(2)
    else:
        video_match = short_url_video_id_re.search(url)
        if video_match:
            video_id = video_match.group(2)
        else:
            return False, "", ""


    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=(lang_code,))

    if transcript:
        #print(transcript)
        total_text = reduce(lambda x,y: "{x} {y}".format(x=x, y=y), list(map(lambda x: x["text"], transcript)))
        r= requests.get(url, headers=http_headers)


        soup = BeautifulSoup(r.text, 'lxml')

        title = soup.title.text

        return True, title, total_text
    else:
        print(req.text)
        return False, "", ""

def get_info_from_url(url):
    #print(url)

    youtube_url, title, text = get_captions_text_from_youtube(url)

    if not youtube_url:
        print("Not a youtube url")
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

    print(text)

    if lang != "fr":
        raise InvalidLanguage()

    r = requests.post(settings.BULLSHIT_O_METRE_API, data=text.encode("utf8"))
    pred = r.text

    return title, pred

def evaluate_text(text):

    title = "%s..." % text[:10]

    r = requests.post(settings.BULLSHIT_O_METRE_API, data=text.encode("utf8"))
    pred = r.text

    return title, pred
