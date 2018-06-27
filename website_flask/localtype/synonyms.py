from nltk.corpus import wordnet as wn
import localtype.thesaurus as th

def suggest_synonyms(c, tokenizer, text, cityid, N=6):
    syndict = {}
    basic_prob = c.predict_proba([text])[0][cityid]
    tokens = tuple(tokenizer.tokenize(text.lower()))
    for i,wd in enumerate(tokens):
        if not wn.synsets(wd,pos=wn.ADJ) == []:
            w = th.Word(wd)
            syns = w.synonyms()
            del w
            probs = []
            good_syns = []
            new_tokens = list(tokens)
            for s in syns:
                new_tokens[i] = s
                prob = c.predict_proba([' '.join(new_tokens)])[0][cityid]
                if prob>basic_prob:
                    probs.append(prob)
                    good_syns.append(s)
            ranked_adjs = [x for _,x in sorted(zip(probs,good_syns),reverse=True)]
            syndict[wd] = ranked_adjs[:N]
    return syndict

def html_suggested_synonyms(syndict):
    html = ''
    for w,s in syndict.items():
        if len(s) > 0:
            html += '<p><strong>'+w+':</strong> '
            html += ''.join([sy+', ' for sy in s[:-1]])
            html += s[-1]
            html += '</p>\n'
    return html