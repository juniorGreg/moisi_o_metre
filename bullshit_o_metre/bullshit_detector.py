
import fr_core_news_sm

import pandas as pd

import psycopg2

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

import numpy as np
import json

class BullshitDetector():
    def __init__(self):
        self.vec = TfidfVectorizer(max_features=1000, ngram_range=(1,2))
        self.clf = MultinomialNB()
        self.nlp = fr_core_news_sm.load()
        self.stopwords = self.nlp.Defaults.stop_words


    def clean_text(self, text):
        doc = self.nlp(text)
        lemmas = [token.lemma_ for token in doc if token.pos_ != 'PROPN' and token.is_alpha]
        a_lemmas = [lemma for lemma in lemmas if lemma not in self.stopwords]

        return ' '.join(a_lemmas)


    def predict(self, text):
        data = self.clean_text(text)
        X_data = self.vec.transform([data])
        X = pd.DataFrame(X_data.toarray(), columns=self.vec.get_feature_names())
        preds = self.clf.predict_proba(X)

        return preds

    def load_model(self, path="model.json"):
        with open(path) as file:
            dict_model = json.load(file)

        dict_vec = dict_model["vec"]
        dict_clf = dict_model["clf"]

        self.vec.vocabulary_ = dict_vec["vocabulary_"]
        self.vec.fixed_vocabulary_ = dict_vec["fixed_vocabulary_"]
        self.vec.idf_ = np.asarray(dict_vec["idf_"])
        self.vec.stop_words_ = set(dict_vec["stop_words_"])

        self.clf.class_count_ = np.asarray(dict_clf["class_count_"])
        self.clf.class_log_prior_ = np.asarray(dict_clf["class_log_prior_"])
        self.clf.classes_ = np.asarray(dict_clf["classes_"])
        #self.clf.coef_ = np.asarray(dict_clf["coef_"])
        self.clf.feature_count_ = np.asarray(dict_clf["feature_count_"])
        self.clf.feature_log_prob_ = np.asarray(dict_clf["feature_log_prob_"])
        #self.clf.intercept_ = np.asarray(dict_clf["intercept_"])
        self.clf.n_features_ = np.asarray(dict_clf["n_features_"])
