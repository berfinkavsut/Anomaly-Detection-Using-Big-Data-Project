



import unittest
from models.xstream import xstream
from models.iforest import iForest
import numpy as np
import h5py
import scipy.io

data = scipy.io.loadmat("/Users/egeozanozyedek/Documents/PyCharmProjects/network-anomaly-detection/data/shuttle.mat")
X = np.asarray(data["X"])
Y = np.asarray(data["y"])

length = X.shape[0]
X = X[:length]
Y = Y[:length]

partition = (X.shape[0] * 8 // 10)

X_train = X[:partition]
Y_train = Y[:partition]
X_test = X[partition:]
Y_test = Y[partition:]
print(X_train.shape, Y_train.shape)



detect = xstream(X_train)
fit_score = detect.fit(X_train, Y_train)

val_score = detect.predict(X_test, Y_test)
print(fit_score, '\n', val_score)