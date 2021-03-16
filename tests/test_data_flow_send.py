import scipy.io
import numpy as np
from flow.producer import DataProducer
import time
import pandas as pd

data = scipy.io.loadmat('../data/shuttle.mat')  # %7 anomaly rate
X = np.asarray(data["X"])
Y = np.asarray(data["y"])

# data = np.asarray(pd.read_csv('../data/hello_2'))
# X = np.asarray(data[:, 1:-1])
# Y = np.asarray(data[:, -1])

length = 1000  # X.shape[0]
X_train = X[:length]
Y_train = Y[:length]



p = DataProducer(config="cloud")
s = time.time()
for i in range(length):
    data = X_train[i]

    # data = X_train[i]
    p.send_stream(topic="test-AD", value=data)

e = time.time()

print((e - s) / 60)
