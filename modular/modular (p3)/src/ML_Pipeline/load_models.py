import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import models
from gensim.models import FastText as ft


# Importing Word2Vec
word2vecModel = models.KeyedVectors.load_word2vec_format('../input/GoogleNews-vectors-negative300.bin.gz', binary=True)

# Importing Count Vectorizer
count_vectorizer = CountVectorizer(stop_words='english')

# Importing IFIDF
tfidf_vec = TfidfVectorizer(stop_words='english', analyzer='word', ngram_range=(1,3))

# # Importing FastText
fasttext_model=ft.load_fasttext_format("../input/cc.en.300.bin.gz")

# # Import Glove
glove_df = pd.read_csv('../input/glove.6B.300d.txt', sep=" ",
                       quoting=3, header=None, index_col=0)
glove_model = {key: value.values for key, value in glove_df.T.items()}

# Function for calculating co-ocurrence matrix
def co_ocurrence_mat(input):
    co_ocr_vocab = []
    for i in input:
        [co_ocr_vocab.append(x) for x in i.split()]

    co_occur_vector_matrix = np.zeros((len(co_ocr_vocab), len(co_ocr_vocab)))

    for _, sent in enumerate(input):
        words = sent.split()
        for index, word in enumerate(words):
            if index != len(words)-1:
                co_occur_vector_matrix[co_ocr_vocab.index(word)][co_ocr_vocab.index(words[index+1])] += 1   


    return  co_occur_vector_matrix, co_ocr_vocab       