import numpy as np
import pandas as pd

from matplotlib import pyplot
from sklearn.cluster import KMeans

from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor


class ClusterExtractor(BaseFeatureExtractor):
    """
    IMPORTANT NOTES
    Clustering is based on batch learning.
    Not compatible with online learning.

    to be added: max iterations, tolerance  for k-means model
    """

    feature_extractor_name = 'cluster_extractor'

    def __init__(self, param, selected_features):
        super().__init__(param=param, selected_features=selected_features)
        self.cluster_no = self.param['cluster_no']
        self.model = KMeans(n_clusters=self.cluster_no)

    def fit(self, X):
        """
        Select a subset of X with respect to selected features before.
        Fit and train k-means clustering model.

        :param X: data frame input
        :return:
        """

        X = X[self.selected_features]
        X = X.to_numpy()
        self.model.fit(X)

    def transform(self, X):
        """
        Select a subset of X with respect to selected features before.
        Predict cluster ids of X.
        Return output of k-means clustering model.

        :param X: data frame input
        :return: data frame cluster ids
        """

        X = X[self.selected_features]
        X = X.to_numpy()

        # assign a cluster to each example
        pred_cluster_ids = self.model.predict(X)

        # retrieve predicted cluster ids
        self.features_extracted = np.array(pred_cluster_ids)

        """"
        if 0:
            pred_clusters = np.unique(pred_cluster_ids)
            for cluster in pred_clusters:
                # get row indexes for samples with this cluster
                row_ix = np.where(pred_cluster_ids == cluster)
                # create scatter of these samples
                pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
            # show the plot
            pyplot.show()
        """

        return self.features_extracted

    def fit_transform(self, X):
        """
        Select a subset of X with respect to selected features before.
        Fit and train k-means clustering model.
        Predict cluster ids of X.
        Return output of k-means clustering model.

        :param X: data frame input
        :return: data frame cluster ids
        """

        self.fit(X)
        self.features_extracted = self.transform(X)
        return self.features_extracted
