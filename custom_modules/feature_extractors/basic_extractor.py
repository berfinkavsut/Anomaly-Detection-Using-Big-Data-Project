import pandas as pd
from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor


class BasicExtractor(BaseFeatureExtractor):

    feature_extractor_name = 'basic_extractor'

    def __init__(self, param, selected_features):
        """
        :param param: dictionary for model parameters
        :param selected_features: selected features to extract features
        """

        super().__init__(param=param, selected_features=selected_features)

    def fit(self, X):
        pass

    def transform(self, X):
        """
        Select a subset of X with respect to selected features before.
        Reduce dimensionality of input.

        :param X: data frame input
        :return: data frame output, subset of input
        """

        features_extracted = X[self.selected_features]
        self.features_extracted = features_extracted.to_numpy()
        return self.features_extracted

    def fit_transform(self, X):
        """
        Select a subset of X with respect to selected features before.
        Reduce dimensionality of input.

        :param X: data frame input
        :return: data frame output, subset of input
        """

        self.fit(X)
        self.features_extracted = self.transform(X)
        return self.features_extracted
