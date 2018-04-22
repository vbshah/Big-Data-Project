# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 18:35:51 2018

@author: vbshah
"""
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from nltk.tokenize import sent_tokenize, word_tokenize
import pickle

"""
Column names
Date received	Product	Sub-product	Issue	Sub-issue	Consumer complaint narrative	Company public response	Company	State	ZIP code	Tags	Consumer consent provided?	Submitted via	Date sent to company	Company response to consumer	Timely response?	Consumer disputed?	Complaint ID
"""
# data = pd.read_csv('Consumer_Complaints (1).csv')

ps = PorterStemmer()
def clean_data(s):
    ls = word_tokenize(s)
    unique_words = [ps.stem(i) for i in ls if i.isalpha()]
    return ' '.join(list(set(unique_words)))        
data = data
print(len(data))
# stop_words = set(stopwords.words('english'))
f = open('stop_words.txt.txt')
stop_words = [i.strip('\n') for i in f.readlines()]
vectorizer = TfidfVectorizer(stop_words = stop_words, use_idf = True, max_features = 500)
issues = ['Loan modification,collection,foreclosure', 'Incorrect information on credit report',
          'Loan servicing, payments, escrow account', "Cont'd attempts collect debt not owed",
          'Incorrect information on your report', 'Account opening, closing, or management',
          'Disclosure verification of debt', 'Communication tactics', 'Deposits and withdrawals',
          "Problem with a credit reporting company's investigation into an existing problem"
          ]
issues = set(issues)
issue_dict = []
complaint_nrrative = []
for i in range(len(data)):
    if data['Issue'][i] in issues:
        s = data['Consumer complaint narrative'][i]
        if type(s) == str and len(s) > 0:
            s = clean_data(s)
            complaint_nrrative.append(s)
            issue_dict.append(len(s))
x = vectorizer.fit_transform(complaint_nrrative)
with open('sparse_dense.pkl', 'wb') as f:
    pickle.dump(x.todense(), f)
print('data stored in sparse_dense.pkl')
