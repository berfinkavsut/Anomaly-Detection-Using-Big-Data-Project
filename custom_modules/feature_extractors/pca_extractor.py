import pandas as pd

from sklearn.decomposition import PCA

from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor


class PCAExtractor(BaseFeatureExtractor):

    feature_extractor_name = 'pca_extractor'

    def __init__(self, param, selected_features):
        """
        :param param: dictionary for model parameters
        :param selected_features: selected features to extract features
        """

        super().__init__(param=param, selected_features=selected_features)

        self.k = self.param['k']
        self.model = PCA(n_components=self.k)
        # print('k: ', self.k)

    def fit(self, X):
        """
        Select a subset of X with respect to selected features before.
        Fit X on PCA model.

        :param X: data frame input
        :return:
        """

        X = X[self.selected_features]
        X = X.to_numpy()
        self.model.fit(X)

    def transform(self, X):
        """
        Select a subset of X with respect to selected features before.
        Reduce dimensionality of input with PCA.
        Return output of PCA with lower dimension.

        :param X: data frame input
        :return: data frame output of PCA
        """

        X = X[self.selected_features]
        X = X.to_numpy()
        features_extracted = self.model.transform(X)
        self.features_extracted = pd.DataFrame(features_extracted)
        return self.features_extracted

    def fit_transform(self, X):
        """
        Select a subset of X with respect to selected features before.
        Fit X on PCA model.
        Reduce dimensionality of input with PCA.
        Return output of PCA with lower dimension.

        :param X: data frame input
        :return: data frame output of PCA
        """

        self.fit(X)
        self.features_extracted = self.transform(X)
        return self.features_extracted

    def get_model(self):
        """
        Get the model for double check.

        :return: PCA model
        """
        return self.model
