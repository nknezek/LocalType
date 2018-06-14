#!/usr/bin/env python
from localtype import app

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from lime.lime_text import LimeTextExplainer
import dill

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
stemmer = SnowballStemmer('english')
tfidf_vectorizer = dill.load(open('/Users/nknezek/Documents/Insight_local/project/3city_test/tfidf_vectorizer.m', 'rb'))
c = dill.load(open("/Users/nknezek/Documents/Insight_local/project/3city_test/trained_pipeline.m", 'rb'))


app.run(debug=True)
