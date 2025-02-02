import numpy as np
from nltk import pos_tag, ne_chunk
from nltk.probability import FreqDist
from collections import namedtuple, Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from pandas.core.arrays.numpy_ import PandasArray
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.util import ngrams


def _reviews(df):
    words = list()

    for i in df["Review"]:
        for j in i:
            words.append(j)
    return words


def bow(df):
    """bag of words"""
    bag = np.zeros(len(df['Review']), dtype=np.float64)
    for i in df['Review']:
        for k, j in enumerate(i):
            if j in i:
                bag[k] = 1
    return bag


def frequency_distribution(df, len_fd: int = 10):
    """frequency distribution"""

    fd = namedtuple("fd", ["most_common", "chart", "all"])
    words = _reviews(df)

    f_dist = FreqDist(words)
    fd.all = f_dist
    fd.most_common = f_dist.most_common(len_fd)
    fd.chart = f_dist.plot(10)
    return fd


def word_cloud(df):
    """words & tags cloud from most common frequencies"""

    words = _reviews(df)
    word_could_dict = Counter(words)

    wc = WordCloud().generate_from_frequencies(word_could_dict)

    plt.figure(figsize=(12, 12))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()


def pos_tagging(df):
    """PoS tagging"""
    words = _reviews(df)
    return pos_tag(words)


def ner(df):
    """Named entity recognition"""
    pos_tagged_words = pos_tagging(df)
    ner = ne_chunk(pos_tagged_words, binary=False)
    return ner


def count_vectorizer(df: PandasArray):
    """Count Vectorizer"""
    review_df = df['Review']
    reviews = [i for i in review_df]

    cv = CountVectorizer()
    review = [''.join(str(item)) for item in reviews]
    cv_tf = cv.fit_transform(review)

    return cv_tf, cv.get_feature_names(), cv.ngram_range


def terms_frequency(df: PandasArray):
    """TF-IDF"""
    reviews = df['Review']
    tf_vectorizer = TfidfVectorizer(norm=None)
    _tf_idf = namedtuple("_cv", ["vocab", "feature_names", "output"])

    review = [''.join(str(item)) for item in reviews]

    # Generating output for TF_IDF
    _tf_idf.output = tf_vectorizer.fit_transform(review)
    _tf_idf.vocab = tf_vectorizer.vocabulary_
    _tf_idf.feature_names = tf_vectorizer.get_feature_names()

    return _tf_idf


def n_gram(n, df: PandasArray):
    """NGram: assigning the probability to the next word"""
    reviews = df
    return dict([(word, True) for word in ngrams(reviews, n)])
