#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 15:21:38 2021

@author: user
"""
import numpy as np
import pandas as pd
import sys

from sklearn import tree
from sklearn.model_selection import train_test_split 
from sklearn import metrics



c_dict={ 'C':0, 'D':1, 'H':2,'S':3}

def card2val(l):
    n=[]
    n1=int(l[2:4])
    n2=int(l[9:11])
    n3= int(l[16:18])
    n.append(n1)
    n.append(n2)
    n.append(n3)
    k=[]
    for i in n:
        k.append(n.count(i))
    same_num=max(k)
    pp=max(n[:3])
    for i in range(3):
        if k[i]==same_num:
            pp=n[i]
        
    n.append(same_num)
    n.append(pp)
        
    return n
    n=[0,0,0,0,0,0]
    n[0]=int(l[2:4])
    n[1]=c_dict[l[4]]
    n[2]=int(l[9:11])
    n[3]=c_dict[l[11]]
    n[4]=int(l[16:18])
    n[5]=c_dict[l[18]]
    
    return n

column_names = ["hand", "value", "handtype", "score"]    
df = pd.read_csv("data13_3.csv", names=column_names,skiprows=1)
dataset = df.values
hand = df.hand.to_list()
#X = hand

#l = X[0]
#print(X[0])
nn = []
for i in hand:
    nn.append(card2val(i))
#nnn = np.asarray(nn)
X=nn
Y = dataset[:, 3]
Y=Y.astype('int') 
for i in range(100):
    print(X[i])
print(Y)

#sys.exit()
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

m = np.array([13,6,5,1,13])
mynum = m.reshape(1, -1)
#array.reshape(1, -1)
print(iris_clf.predict(mynum))

from sklearn import neighbors

clf = neighbors.KNeighborsClassifier()
iris_clf = clf.fit(train_X, train_y)

# 預測
test_y_predicted = iris_clf.predict(test_X)
print(test_y_predicted)

# 標準答案
print(test_y)
m = np.array([13,6,5, 1, 13])
mynum = m.reshape(1, -1)
#array.reshape(1, -1)
print(iris_clf.predict(mynum))

'''
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