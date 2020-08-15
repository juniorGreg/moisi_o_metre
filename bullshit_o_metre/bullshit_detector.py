
import spacy

import pandas as pd

import psycopg2

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

class BullshitDetector():
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1,2))
        self.clf = MultinomialNB()
        self.nlp = spacy.load('fr_core_news_sm')
        self.stopwords = self.nlp.Defaults.stop_words


    def clean_text(self, text):
        doc = self.nlp(text)
        lemmas = [token.lemma_ for token in doc if token.pos_ != 'PROPN' and token.is_alpha]
        a_lemmas = [lemma for lemma in lemmas if lemma not in self.stopwords]

        return ' '.join(a_lemmas)


    def predict(self, text):
        data = self.clean_text(text)
        X_data = self.vectorizer.transform([data])
        X = pd.DataFrame(X_data.toarray(), columns=self.vectorizer.get_feature_names())
        preds = self.clf.predict_proba(X)

        return preds
