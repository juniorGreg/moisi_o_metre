
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import spacy
from collections import Counter
from langdetect import detect
from .models import *
import asyncio

from multiprocessing import Process, Queue

def retrieve_text_from_website(q, url):
    asyncio.set_event_loop(asyncio.new_event_loop())

    session = HTMLSession()
    r = session.get(url)
    r.html.render()

    q.put(r.html.html)





def evaluate_website(url, recalculate=False):
    website = RecordedWebSite.objects.filter(url=url).first()
    if website:
        if recalculate:
            print("recalcul")
            website.score = score_website(website.meaningful_lemmas.all(), website.lemmas_count)
            website.save()
        return website

    queue = Queue()
    p = Process(target= retrieve_text_from_website, args=(queue, url))
    p.daemon = True
    p.start()
    p.join()
    result = queue.get()

    #print(result)

    soup = BeautifulSoup(result, 'lxml')
    #print(soup.find_all('p')[0].text)

    text = ""
    for tag in soup.find_all("p"):
        text += " "
        text += tag.text

    intab = "0123456789?!:"
    outtab = "          .. "

    trans = str.maketrans(intab, outtab)

    text = text.translate(trans)
    text = " ".join(text.split())
    #print(text)
    if len(text) < 100:
        print("text to short")
        return None

    lang = detect(text[:100])
    print(lang)

    if lang != 'fr':
        return None

    title = soup.h1.text
    print(title)

    # download french model --> python3 -m spacy download fr_core_news_md
    nlp = spacy.load("fr_core_news_sm")
    nlp.begin_training()
    #print(self.text)
    doc = nlp(text)

    #print(doc)
    lemmas = [token.lemma_ for token in doc if not token.lemma_.isdigit()]
    #print(lemmas)

    counter = Counter(lemmas)

    filtered_lemmas = [key for key, value in counter.items() if value == 1]
    meaningful_lemmas = []
    lemmas_count=len(lemmas)
    print(lemmas_count)
    website = RecordedWebSite.objects.create(title=title, url=url, lemmas_count=lemmas_count)

    for lemma in filtered_lemmas:
        tainted_lemma = TaintedLemma.objects.filter(name=lemma)
        if tainted_lemma:
            meaningful_lemmas.append(tainted_lemma[0])
        else:
            new_tainted_lemma = TaintedLemma.objects.create(name=lemma)
            meaningful_lemmas.append(new_tainted_lemma)

    website.meaningful_lemmas.set(meaningful_lemmas)

    score = score_website(meaningful_lemmas, lemmas_count)
    website.score = score
    website.save()
    return website

def score_website(meaningful_lemmas, lemmas_count):
    if lemmas_count == 0:
        return 0
    evaluate_meaningful_lemmas = [lemma for lemma in meaningful_lemmas if lemma.is_evaluated]
    evaluate_meaningful_lemmas_neutral = [lemma for lemma in evaluate_meaningful_lemmas if lemma.type == 'NEU']
    tainted_meaningful_lemma_count = len(evaluate_meaningful_lemmas) - len(evaluate_meaningful_lemmas_neutral)

    return tainted_meaningful_lemma_count/lemmas_count
