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

import localtype.synonyms as syn
import localtype.lime_custom_output as lmc

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
stemmer = SnowballStemmer('english')
tfidf_vectorizer = dill.load(open('/Users/nknezek/Documents/Insight_local/project/3city_test/tfidf_vectorizer.m', 'rb'))
c = dill.load(open("/Users/nknezek/Documents/Insight_local/project/3city_test/trained_pipeline.m", 'rb'))

# Load the text-analysis model

statetowns = ['AK/Anchorage/', 'CA/Berkeley/', 'TX/Denton/']
explainer = LimeTextExplainer(class_names=statetowns)

def make_dropdown(towns, selected = 0):
    dropdown_html = "<select id=\"input_city\" name=\"input_city\">\n"
    for i,town in enumerate(towns):
        if i==selected:
            dropdown_html += "<option selected value=\"{}\">{}</option>\n".format(i,town)
        else:
            dropdown_html += "<option value=\"{}\">{}</option>\n".format(i, town)
    dropdown_html += "</select>\n"
    return dropdown_html

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title='LocalType',
                           )

@app.route('/output')
def text_output():
    # pull input text and city from input field and store it
    input_city = request.args.get('input_city')
    dropdown_html = make_dropdown(statetowns,int(input_city))
    try:
        input_text = request.args.get('input_text')
    except:
        input_text = "you didn't enter any text! So instead you get to see this easter-egg! Aren't you lucky?"
    syndict = syn.suggest_synonyms(c,tokenizer,input_text,int(input_city))
    synhtml = syn.html_suggested_synonyms(syndict)
    exp = explainer.explain_instance(input_text, c.predict_proba, num_features=6, labels=[int(input_city)])
    color_text = lmc.color_words(exp)
    # color_text = "<p>color text</p>"
    score = lmc.colored_score(exp,int(input_city))
    # top_cities = lmc.plot_cityscores(exp,int(input_city))
    top_cities = lmc.list_cities(exp,int(input_city))
    # top_cities = "<p>top cities</p>"

    top_words = lmc.plot_top_words(exp)
    # top_words = "<p>top words</p>"
    return render_template("output.html", score=score, input_text=input_text, dropdown_html=dropdown_html, color_text=color_text, top_words=top_words, top_cities=top_cities, synonyms=synhtml)

