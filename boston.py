#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 09:21:47 2021

@author: user
"""

from sklearn.datasets import load_boston
boston = load_boston()
boston.keys()

print(boston.DESCR)

boston.data.shape

import pandas as pd
pd.DataFrame(boston.data)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(boston.data,boston.target,test_size=0.3)
print(x_train.shape,y_train.shape)

from sklearn.linear_model import LinearRegression#建立模型
mlr = LinearRegression()
mlr.fit(x_train,y_train)
print('係數',mlr.coef_,"\n截距",mlr.intercept_)

#檢測模型好壞
from sklearn.metrics import regression
y_predict = mlr.predict(x_test)

print('線性迴歸模型：')
print("預測的均方誤差：",regression.mean_squared_error(y_test,y_predict))
print("預測的平均絕對誤差：",regression.mean_absolute_error(y_test,y_predict))

print("模型的分數：",mlr.score(x_test,y_test))

from sklearn.preprocessing import PolynomialFeatures

# 多項式化
poly2 =PolynomialFeatures(degree=2)
x_poly_train = poly2.fit_transform(x_train)
x_poly_test = poly2.transform(x_test)

mlrp = LinearRegression()# 建立模型
mlrp.fit(x_poly_train, y_train)

y_predict2 = mlrp.predict(x_poly_test)# 測模型好壞
print("多項式迴歸模型：")
print("預測的均方誤差：",regression.mean_squared_error(y_test,y_predict2))
print("預測平均絕對誤差：",regression.mean_absolute_error(y_test,y_predict2))

print("模型的分數：",mlrp.score(x_poly_test,y_test))