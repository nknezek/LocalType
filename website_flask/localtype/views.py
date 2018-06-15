from flask import render_template
from localtype import app
from flask import request

from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from lime.lime_text import LimeTextExplainer
import dill

import localtype.bokehplot as plt

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
stemmer = SnowballStemmer('english')
tfidf_vectorizer = dill.load(open('/Users/nknezek/Documents/Insight_local/project/3city_test/tfidf_vectorizer.m', 'rb'))
c = dill.load(open("/Users/nknezek/Documents/Insight_local/project/3city_test/trained_pipeline.m", 'rb'))

# Load the text-analysis model

statetowns = ['AK/Anchorage/', 'CA/Berkeley/', 'TX/Denton/']
explainer = LimeTextExplainer(class_names=statetowns)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title='LocalType',
                           )

@app.route('/output')
def text_output():
    # pull input text and city from input field and store it
    input_text = request.args.get('input_text')
    input_city = request.args.get('input_city')
    if input_text is None:
        input_text = "you didn't enter any text! So instead you get to see this easter-egg! Aren't you lucky?"
    exp = explainer.explain_instance(input_text, c.predict_proba, num_features=6, labels=[int(input_city)])
    script, div = plt.create_figure()
    # just select the Cesareans  from the birth dtabase for the month that the user inputs

    return render_template("output.html", input_text=input_text, input_city=input_city, explainer=exp.as_html(), script=script, div=div)

