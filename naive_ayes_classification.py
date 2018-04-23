# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 19:25:25 2018

@author: vbshah
"""

from sklearn.naive_bayes import MultinomialNB
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

with open('target_dump.pkl', 'rb') as f:
    target = pickle.load(f)
with open('sparse_dense.pkl', 'rb') as f:
    training_data = pickle.load(f)
    
issues = ["Problem with a credit reporting company's investigation into an existing problem",
 'Account opening, closing, or management',
 'Incorrect information on credit report',
 'Loan servicing, payments, escrow account',
 'Incorrect information on your report',
 "Cont'd attempts collect debt not owed",
 'Loan modification,collection,foreclosure',
 'Deposits and withdrawals',
 'Disclosure verification of debt',
 'Communication tactics']

x_train, x_test, y_train, y_test = train_test_split(training_data, target, test_size = 0.2, 
                                                    random_state = 42)
clf = MultinomialNB().fit(x_train, y_train)
predicted = clf.predict(x_test)
print(accuracy_score(y_test, predicted))