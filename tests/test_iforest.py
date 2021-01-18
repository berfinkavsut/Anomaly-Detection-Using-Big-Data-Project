import unittest
from models.iforest import iForest
import numpy as np

class TestKitNet(unittest.TestCase):
    def setUp(self):
        num_features = 20
        n = 1
        X = np.random.rand(n, num_features)
        y = np.random.randint(0, 2, (n, 1))
        self.model = iForest(X)
        self.auroc, self.scores = self.model.fit(X,y)
        # print(np.where(np.isnan(self.scores)))

    def test_fit_shape(self):
        # print("=======nan=====:",np.where(np.isnan(self.scores)))
        self.assertEqual(len(self.scores), 1)

    def test_fit_range(self):
        self.assertTrue(self.auroc() >= 0)

