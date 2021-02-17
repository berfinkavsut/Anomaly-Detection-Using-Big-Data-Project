import unittest
from train import Train
import numpy as np
from tests.plot_for_p3 import plot_for_p3
import scipy.io

class MyTestCase(unittest.TestCase):
    def setUp(self):
        props = {'xStream': {}, 'IForest': {}, 'Loda': {'contamination': 0.2}}
        ens_props = {'Ensemble (Loda with Contamination: 0.3, IForest)': {'Loda': {'contamination': 0.3}, 'IForest': {}},
                     'Ensemble (Loda with Contamination: 0.1, IForest)': {'Loda': {'contamination': 0.1}, 'IForest': {} }}
        self.train = Train(num_features=9, model_properties=props, ensemble_model_properties=ens_props)
        data = scipy.io.loadmat('../data/shuttle.mat')  # %7 anomaly rate
        X = np.asarray(data["X"])
        Y = np.asarray(data["y"])
        length = 10000  # X.shape[0]
        self.X_train = X[:length]
        self.Y_train = Y[:length]

    def test_something(self):
        self.train.fit(self.X_train)
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
