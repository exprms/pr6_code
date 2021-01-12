import functions
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords

# base file for RSS sources
url_frame = pd.read_excel('Feeds.xlsx', skiprows=0, header=1)

# schreibe alle titel in eine liste und entferne duplikate - siehe functions.py
title_list = functions.get_titles(url_frame.URL.to_list())

# Teil 1:
# Finde die ähnlichen tTitel -----------------------------------------------------------------------
# source: https://towardsdatascience.com/how-to-rank-text-content-by-semantic-similarity-4d2419a84c32

stop_words = set(stopwords.words('english'))

# Interface lemma tokenizer from nltk with sklearn
class LemmaTokenizer:
    ignore_tokens = [',', '.', ';', ':', '"', '``', "''", '`']
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc) if t not in self.ignore_tokens]

# Lemmatize the stop words
tokenizer = LemmaTokenizer()
token_stop = tokenizer(' '.join(stop_words))

# Create TF-idf model
vectorizer = TfidfVectorizer(stop_words=token_stop,
                              tokenizer=tokenizer)
doc_vectors = vectorizer.fit_transform(title_list)

# Calculate similarity
cosine_similarities = linear_kernel(doc_vectors, doc_vectors).flatten()
#cosine_similarities2 = cosine_similarity(doc_vectors, doc_vectors).flatten()

# Ausgabe der Indizes mit Ähnlichkeiten
reference_news, similar_news, cosine_value = functions.get_articles(cosine_similarities, title_list, 0.7)

# Schreibe ähnliche Titel in einen dataframe
match = pd.DataFrame([[cosine_value[i],
                       title_list[reference_news[i]],
                       title_list[similar_news[i]]] for i in range(len(reference_news))],
                     columns=['cosine_sim', 'title_1', 'titel_2'])

# Teil 2
# Filtere nach Schlagwörter

schlagwort_list = ['Corona', 'corona', 'Covid', 'covid', 'COVID', 'CORONA']
selected_titles = []
for item in schlagwort_list:
    selected_titles += [tit for tit in title_list if item in tit]

# Entferne alle " und ', und binde zu einem Text zusammen
selected_titles = [str.replace("'","") for str in selected_titles]
selected_titles = [str.replace('"','') for str in selected_titles]
text = '. '.join(selected_titles)
text = text.replace('?. ','? ')
text = text.replace('!. ','! ')



