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
import requests
import ast
from tqdm import tqdm

class InsightsEngine():
    def __init__(self):
        self.data = None
        self.df = pd.DataFrame([], columns=['JOURNAL_ID', 'TEXT'])
        self.nlp = None
        self.apiRoute = 'http://localhost:5000/api/sendSearch'
        self.data_dict = {}
        self.toolbar_width = 1
        self.jnl_content = ''
        self.intern_id = None

    def get_data(self):
        # fetch the data, and show progress
        for i in tqdm(range(self.toolbar_width)):
            self.data = requests.get(self.apiRoute).json()
        try:
            self.data = self.data['entities']
            for BE in self.data:
                for BEAttrs in BE['baseEntityAttributes']:
                    if BEAttrs['attributeCode'] == "PRI_JOURNAL_LEARNING_OUTCOMES":
                        if len(BEAttrs['valueString']) > 0:
                            self.jnl_content = BEAttrs['valueString']

                    if BEAttrs['attributeCode'] == "PRI_JOURNAL_TASKS":
                        if len(BEAttrs['valueString']) > 0:
                            self.jnl_content += " " + BEAttrs['valueString']

                    if BEAttrs['attributeCode'] == "LNK_INTERN":
                        x = ast.literal_eval(BEAttrs['valueString'])
                        self.intern_id = x[0]
                        if self.intern_id != None:
                            entity_code = BE['code']
                # do not take in journals that are empty or have no intern attached
                if self.intern_id != None and len(self.jnl_content) > 0:
                    self.data_dict[(entity_code, self.intern_id)] = self.jnl_content
                else:
                    continue
            return(self.data_dict)
        except:
            return(f"{self.data} has empty entities. Please check the SearchBE")

    def make_dataframe(self, data_dict):
        i = 0
        for key, value in data_dict.items():
            value = value.replace('\n', " ")
            value = value.replace('.', " ")
            cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
            cleantext = re.sub(cleanr, '', value)
            cleantext = cleantext.lower()
            self.df.loc[i,'JOURNAL_ID'] = key[0]
            self.df.loc[i,'TEXT'] = cleantext
            i+=1
        return self.df

    def load_language_model(self, size='large'):
        if size == 'large':
            # load in nlp language model
            self.nlp = spacy.load('en_core_web_lg')
        if size == 'small':
            self.nlp = spacy.load('en_core_web_sm')

    def remove_empty(self, df):
        if type(df) == pd.DataFrame:
            drop_idx = []
            for idx, row in df.iterrows():
                if len(row.TEXT) == 0:
                    drop_idx.append(idx)
            if len(drop_idx) > 0:
                self.df = df.drop(drop_idx)
                return self.df
            else:
                return(f"DataFrame does not have empty rows")
        else:
            return ("Please use a Pandas DataFrame Object")

    def remove_stopwords(self, field=None):
        # remove stopwords
        self.df[field] = self.df[field].apply(lambda text:" ".join\
                        (token.lemma_ for token in self.nlp(text) if not token.is_stop))
        return self.df

    def remote_punctuations(self, field=None):
        # remove punctionations
        self.df[field] = self.df[field].apply(lambda text:" ".join\
                        (token.lemma_ for token in self.nlp(text) if not token.is_punct))
        return self.df

    def remove_numbers(self, field=None):
        # remove numbers
        self.df[field] = self.df[field].apply(lambda text:" ".join\
                        (token.lemma_ for token in self.nlp(text) if not token.like_num))
        return self.df

    def remove_spaces(self, field=None):
        # remove white spaces
        self.df[field] = self.df[field].apply(lambda text:" ".join\
                        (token.lemma_ for token in self.nlp(text) if not token.is_space))
        return self.df
    def extract_pos(self, field=None):
        # make a new col for POS tags
        self.df['POS'] = self.df[field].apply(lambda text:",".join\
                                                (token.pos_ for token in self.nlp(text)))

    def extract_lemma(self, field=None):
        # make a new col for Lemma
        self.df['LEMMA'] = self.df[field].apply(lambda text:",".join\
                                                (token.lemma_ for token in self.nlp(text)))
    
