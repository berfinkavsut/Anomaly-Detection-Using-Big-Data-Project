import scipy.io
import numpy as np
from flow.producer import DataProducer
import time


data = scipy.io.loadmat('../data/shuttle.mat')  # %7 anomaly rate
X = np.asarray(data["X"])
Y = np.asarray(data["y"])
length = 10000  # X.shape[0]
X_train = X[:length]
Y_train = Y[:length]



p = DataProducer()
s = time.time()
for i in range(length):
    data = (X_train[i], Y_train[i])

    # data = X_train[i]
    p.send_stream(topic="Test", value=data)

e = time.time()

print((e-s)/60)