import pandas as pd
import numpy as np
import pickle
import re
import gensim
import nltk
from nltk.stem.porter import *
from gensim.utils import simple_preprocess
import spacy
import random
from wordcloud import WordCloud
import seaborn as sns
import circlify
import json

class InsightsEngine():
    def __init__(self, data):
        self.data = data
        self.df = pd.DataFrame([], columns=['JOURNAL_ID', 'TEXT'])
        self.nlp = None

    def clean_data(self):
        i = 0
        for key, value in self.data.items():
            value = value.replace('\n', " ")
            value = value.replace('.', " ")
            cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
            cleantext = re.sub(cleanr, '', value)
            cleantext = cleantext.lower()
            self.df.loc[i,'JOURNAL_ID'] = key[0]
            self.df.loc[i,'TEXT'] = cleantext
            i+=1
        return df

    def load_language_model(self, size='large'):
        if size == 'large':
            # load in nlp language model
            self.nlp = spacy.load('en_core_web_lg')
        if size == 'small':
            self.nlp = spacy.load('en_core_web_lg')

    def remove_stopwords(self):
        # remove stopwords
        self.df['TEXT'] = self.df.TEXT.apply(lambda text:" ".join\
                        (token.lemma_ for token in self.nlp(text) if not token.is_stop))
        # remove punctionations
        self.df['TEXT'] = self.df.TEXT.apply(lambda text:" ".join\
                        (token.lemma_ for token in self.nlp(text) if not token.is_punct))
        # remove numbers
        self.df['TEXT'] = self.df.TEXT.apply(lambda text:" ".join\
                        (token.lemma_ for token in self.nlp(text) if not token.like_num))

        df['TEXT'] = df.TEXT.apply(lambda text:" ".join\
                        (token.lemma_ for token in self.nlp(text) if not token.is_space))
