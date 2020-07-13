
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import spacy
from collections import Counter
from langdetect import detect
from .models import *




def evaluate_website(url):
    websites = RecordedWebSite.objects.filter(url=url)
    if websites:
        return websites[0]

    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    soup = BeautifulSoup(r.html.html, 'lxml')
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
    print(text)
    if len(text) < 100:
        print("text to short")
        return

    lang = detect(text[:100])
    print(lang)

    title = soup.title.text

    # download french model --> python3 -m spacy download fr_core_news_md
    nlp = spacy.load("fr_core_news_sm")
    nlp.begin_training()
    #print(self.text)
    doc = nlp(text)

    print(doc)
    lemmas = [token.lemma_ for token in doc if not token.lemma_.isdigit()]
    print(lemmas)

    counter = Counter(lemmas)

    filtered_lemmas = [key for key, value in counter.items() if value == 1]
    meaningful_lemmas = []

    for lemma in filtered_lemmas:
        tainted_lemma = TaintedLemma.objects.filter(name=lemma)
        if tainted_lemma:
            meaningful_lemmas.append(tainted_lemma[0])
        else:
            new_tainted_lemma = TaintedLemma.objects.create(name=name)
            meaningful_lemmas.append(new_tainted_lemma)

    website = RecordedWebSite.objects.create(title=title, url=url, meaningful_lemmas=meaningful_lemmas, lemmas_count=len(lemmas))
    return website

def score_website(website):
    pass
