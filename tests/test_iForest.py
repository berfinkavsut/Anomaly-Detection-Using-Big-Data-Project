import unittest
from models.iForest import IForest
from models.loda import Loda
from models.xStream import XStream
import scipy.io
import numpy as np
from tests.plot_for_p3 import plot_for_p3

class TestIForest(unittest.TestCase):
    """
    TestIForest class which inherits unittest and tests the iForest AD class
    """

    def setUp(self):
        data = scipy.io.loadmat('../data/shuttle.mat')  # %7 anomaly rate
        X = np.asarray(data["X"])
        Y = np.asarray(data["y"])
        length = 10000 #X.shape[0]
        self.X_train = X[:length]
        self.Y_train = Y[:length]
        self.model = IForest()
        self.scores, self.probs = self.model.fit_predict(self.X_train)

    def test_fit_predict(self):
        scores = self.scores
        probs = self.probs
        print(probs)
        acc = (self.Y_train == np.round(probs)).mean()
        print(f"Scores: {scores.shape}\nProbs: {probs.shape}\nAcc: {acc}")
        plot_for_p3(probs, self.Y_train, "IForest")
