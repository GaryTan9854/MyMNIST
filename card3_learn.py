#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 13:04:33 2021

@author: user
"""
import numpy as np
import pandas as pd


from sklearn import tree
from sklearn.model_selection import train_test_split 
from sklearn import metrics

dataframe = pd.read_csv("mycard3.csv", header=None)
dataset = dataframe.values
X = dataset[:, 0:3].astype(float)
Y = dataset[:, 3]
print(X)
print(Y)
# 切分訓練與測試資料
train_X, test_X, train_y, test_y = train_test_split(X, Y, test_size = 0.3)

# 建立分類器
clf = tree.DecisionTreeClassifier()
iris_clf = clf.fit(train_X, train_y)

# 預測
test_y_predicted = iris_clf.predict(test_X)
print(test_y_predicted)

# 標準答案
print(test_y)
accuracy = metrics.accuracy_score(test_y, test_y_predicted)
print(accuracy)

m = np.array([7,7,7])
mynum = m.reshape(1, -1)
#array.reshape(1, -1)
print(iris_clf.predict(mynum))


'''
from sklearn import neighbors

clf = neighbors.KNeighborsClassifier()
iris_clf = clf.fit(train_X, train_y)

# 預測
test_y_predicted = iris_clf.predict(test_X)
print(test_y_predicted)

# 標準答案
print(test_y)

#range = np.arange(1, round(0.2 * train_X.shape[0]) + 1)
range = np.arange(1,3)
accuracies = []

#print(range)
for i in range:
    clf = neighbors.KNeighborsClassifier(n_neighbors = i)
    iris_clf = clf.fit(train_X, train_y)
    test_y_predicted = iris_clf.predict(test_X)
    accuracy = metrics.accuracy_score(test_y, test_y_predicted)
    accuracies.append(accuracy)

import matplotlib.pyplot as plt
# 視覺化
plt.scatter(range, accuracies)
plt.show()
appr_k = accuracies.index(max(accuracies)) + 1
print(appr_k)
'''

'''
## randomforest
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=1000)
model.fit(train_X, train_y)
ypred = model.predict(test_X)

print(metrics.classification_report(ypred, test_y))

from sklearn.metrics import confusion_matrix
import seaborn as sns

mat = confusion_matrix(test_y, ypred)
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False)
plt.xlabel('true label')
plt.ylabel('predicted label');
'''
