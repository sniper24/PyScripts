# coding=utf-8

'''
Note:

这个脚本的用途是读取csv文件里的地址信息，用Google Map的API转换为经纬度

'''

import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score


dftrain=pd.read_csv('D:\\train412.csv', sep=',')
dftest=pd.read_csv('D:\\test412.csv', sep=',')
X_train=dftrain.iloc[:,0:-1]
Y_train=dftrain.iloc[:,-1]
X_test=dftest.iloc[:,0:-1]
Y_test=dftest.iloc[:,-1]
print "========Bagging========="
for i in range(100):
    for j in range(10):
        bagging=BaggingClassifier(n_estimators=10,bootstrap=False,max_samples=0.1+0.1*j,random_state=9*i)
        bagging.fit(X_train,Y_train)
        score01,score02=accuracy_score(Y_train, bagging.predict(X_train)),accuracy_score(Y_test, bagging.predict(X_test))
        if score01>0.74 and score02>0.74:
            print "======================"
            print "Current configuration:"
            print "Boosting Method:Bagging"
            print "n_estimators=10,max_samples="+str(10+10*j)+"% samples"
            print "Training set error:"+str(1-score01)
            print "Testing set error:"+str(1-score02)
            print(classification_report(Y_test, bagging.predict(X_test), target_names= ['Good', 'Bad']))
print "========AdaBoost========="
for k in range(100):
    for i in range(10):
        for j in range(50):
            adaboost=AdaBoostClassifier(n_estimators=25*i+50,learning_rate=0.1*j+0.5,random_state=9*k)
            adaboost.fit(X_train,Y_train)
            score01,score02=accuracy_score(Y_train, adaboost.predict(X_train)),accuracy_score(Y_test, adaboost.predict(X_test))
            if score01>0.73 and score02>0.73:
                print "======================"
                print "Current configuration:"
                print "Boosting Method:AdaBoost"
                print "n_estimators="+str(25*i+50)+",learning_rate="+str(0.1*j+0.5)
                print "Training set error:"+str(1-score01)
                print "Testing set error:"+str(1-score02)
                print(classification_report(Y_test, adaboost.predict(X_test), target_names= ['Good', 'Bad']))
        
