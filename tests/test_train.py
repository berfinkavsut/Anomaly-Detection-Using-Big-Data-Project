import unittest
from flow.train import Train
import numpy as np
from tests.plot_for_p3 import plot_for_p3
import scipy.io
import pandas as pd

class MyTestCase(unittest.TestCase):
    def setUp(self):
        props = {'xStream': {}, 'IForest': {}, 'Loda': {}}

        ens_props = {'Ensemble (IForest and Loda)': {'IForest': {}, 'Loda': {}},
                     'Ensemble (Loda and xStream)': {'Loda': {}, 'xStream': {}},
                     'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}}, }
        self.train = Train(num_features=9, model_properties=props, ensemble_model_properties=ens_props)

        # data = scipy.io.loadmat('../data/shuttle.mat')  # %7 anomaly rate
        # X = np.asarray(data["X"])
        # Y = np.asarray(data["y"])

        data = np.asarray(pd.read_csv('../data/hello_2'))
        X = np.asarray(data[:, 1:-1])
        Y = np.asarray(data[:, -1])

        length = 10000  # X.shape[0]
        self.X_train = X[:length]
        self.Y_train = Y[:length]

    def test_something(self):
        for i in range(self.X_train):
            self.train.fit(self.X_train[i])
            a, b = self.train.predict(self.X_train)

        for key in a.keys():
            acc = (self.Y_train == np.round(a[key])).mean()
            print(f"{key}: {acc}%")
            plot_for_p3(a[key], self.Y_train, key)

        for key in b.keys():
            acc = (self.Y_train == np.round(b[key])).mean()
            print(f"{key}: {acc}%")
            plot_for_p3(b[key], self.Y_train, key)



if __name__ == '__main__':
    unittest.main()
