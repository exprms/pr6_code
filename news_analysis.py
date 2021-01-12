import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
# source: https://towardsdatascience.com/how-to-rank-text-content-by-semantic-similarity-4d2419a84c32

# Download stopwords list
#nltk.download('punkt')
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

# read news from text file
input_news = pd.read_csv('feeds.txt', sep='\t', header=0)
valid_news = input_news.loc[input_news['summary']!='None','summary']

search_terms = 'red tomato'
documents = ['cars drive on the road', 'tomatoes are actually fruit']

# Create TF-idf model
vectorizer = TfidfVectorizer(stop_words=token_stop,
                              tokenizer=tokenizer)
doc_vectors = vectorizer.fit_transform(valid_news)

# Calculate similarity
cosine_similarities = linear_kernel(doc_vectors, doc_vectors).flatten()

def get_articles(th):
    # get indices with similarity higher than a given threshold:
    # th = 0.1
    x_temp  = ((cosine_similarities >= th) & (cosine_similarities < 0.999))

    # diagonaleintraege von x_temp
    ignore_index = [number*len(valid_news)+number for number in range(len(valid_news))]

    # nur indizes der oberen dreiecksmatrix ohne diagonale:
    search_index = []
    for i in range(len(valid_news)):
        search_index = search_index + [i*len(valid_news)+j for j in range(i,len(valid_news))]
    search_index = [item for item in search_index if item not in ignore_index]

    # gefundene indizes:
    index_found = [item for item in search_index if x_temp[item]]

    # welche artikelpaare haben eine aehnlichkeit von mehr als th:
    first = [int(np.floor(i/len(valid_news))) for i in index_found]
    second = [np.mod(i, len(valid_news)) for i in index_found]
    return (first, second)

reference_news, similar_news = get_articles(0.4)


#document_scores = [item.item() for item in cosine_similarities[1:]]

