import unittest
from models.loda import Loda
import numpy as np


class TestLoda(unittest.TestCase):
    def setUp(self):
        self.num_features = 5
        self.n = 100
        X = np.random.rand(self.n, self.num_features)

        model = Loda()
        model.fit(X)
        self.scores = model.predict(X)
        self.scores_fit = model.fit_predict(X)

    def test_fit_shape(self):
        self.assertEqual(self.scores[1].shape[0], self.n)  # Probability
        self.assertEqual(self.scores[0].shape[0], self.n)  # Anomaly Score

        self.assertEqual(self.scores_fit[1].shape[0], self.n)  # Probability
        self.assertEqual(self.scores_fit[0].shape[0], self.n)  # Anomaly Score

    def test_fit_range(self):
        self.assertTrue(1 >= self.scores[1].all() >= 0)  # Probability
        self.assertTrue(self.scores[0].all() >= 0)  # Anomaly Score

        self.assertTrue(1 >= self.scores_fit[1][1].all() >= 0)  # Probability
        self.assertTrue(self.scores_fit[1][0].all() >= 0)  # Anomaly Score

