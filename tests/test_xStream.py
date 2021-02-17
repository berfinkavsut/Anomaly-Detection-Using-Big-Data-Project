import unittest
from models.xStream import XStream
import scipy.io
import numpy as np

class TestXStream(unittest.TestCase):
    """
    TestXStream class which inherits unittest and tests the xStream AD class
    """

    def setUp(self):
        data = scipy.io.loadmat('../data/shuttle.mat')  # %7 anomaly rate
        X = np.asarray(data["X"])
        Y = np.asarray(data["y"])
        length = X.shape[0]
        self.X_train = X[:length]
        self.Y_train = Y[:length]
        self.model = XStream()
        self.scores, self.probs = self.model.fit_predict(self.X_train)

    def test_fit_predict(self):
        scores = self.scores
        probs = self.probs
        print(probs)
        acc = (self.Y_train == np.round(probs)).mean()
        print(f"Scores: {scores.shape}\nProbs: {probs.shape}\nAcc: {acc}")