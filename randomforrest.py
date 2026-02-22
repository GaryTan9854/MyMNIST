#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 13:12:36 2021

@author: user
"""

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(random_state=0)
X = [[ 1,  2,  3],  # 2 samples, 3 features
      [11, 12, 13]]
y = [0, 1]  # classes of each sample
clf.fit(X, y)
#RandomForestClassifier(random_state=0)
clf.predict(X)
clf.predict([[4, 5, 6], [14, 15, 16]]) 