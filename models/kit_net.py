"""
Implementation of KitNET autoencoders.
"""
from scipy.stats import norm
import numpy as np
import utils.kitnet_files.KitNET as kit


class KitNet:
    def __init__(self, num_features, maxAE=10, FMgrace=5000, ADgrace=50000):
        """
        :param num_features: Number
        :param maxAE: maximum size for any autoencoder in the ensemble layer
        :param FMgrace: the number of instances taken to learn the feature mapping (the ensemble's architecture)
        :param ADgrace: the number of instances used to train the anomaly detector (ensemble itself)
        """

        self.maxAE = maxAE
        self.FMgrace = FMgrace
        self.ADgrace = ADgrace

        # Build KitNET Model
        self.K = kit.KitNET(num_features, maxAE, FMgrace, ADgrace)

    def fit(self, X):
        """

        :param X:
        :return:
        """
        RMSEs = np.zeros(X.shape[0])
        for i in range(X.shape[0]):
            if i % 1000 == 0:
                print(i)
            RMSEs[i] = self.K.process(X[i, ])

        #benignSample = np.log(RMSEs[self.FMgrace + self.ADgrace + 1:71000])  # ?
        #logProbs = norm.logsf(np.log(RMSEs), np.mean(benignSample), np.std(benignSample))
        return RMSEs
