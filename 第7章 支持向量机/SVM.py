from sklearn.svm import SVC
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
import matplotlib.pyplot as plt


# 使用iris数据集
iris = load_iris()
iris_X = iris.data
iris_Y = iris.target
X_train,X_test,Y_train,Y_test = train_test_split(iris_X, iris_Y, test_size=0.3)

#Support Vector Classifier
clf = SVC(kernel='linear', C=1)
clf.fit(X_train, Y_train)

# train-test score
score = clf.score(X_test, Y_test)
print("train-test score:", score)

# cross-validation score
clf = SVC(kernel='linear', C=1)
score = cross_val_score(clf, iris_X, iris_Y, cv=5)
print("cross-validation score:", score.mean())