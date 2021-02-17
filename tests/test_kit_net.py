import unittest
from models.kit_net import KitNet
import numpy as np


class TestKitNet(unittest.TestCase):
    def setUp(self):
        num_features = 20
        n = 500
        X = np.random.rand(n, num_features)
        model = KitNet(num_features=num_features)
        self.scores = model.fit(X)

    def test_fit_shape(self):
        self.assertEqual(self.scores.shape, (500,))

    def test_fit_range(self):
        self.assertTrue(self.scores.all() >= 0)


