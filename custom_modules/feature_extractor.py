from custom_modules.feature_extractors.autoencoder import Autoencoder
from custom_modules.feature_extractors.cluster_extractor import ClusterExtractor
from custom_modules.feature_extractors.lstm_autoencoder import LSTMAutoencoder
from custom_modules.feature_extractors.pca_extractor import PCAExtractor
from custom_modules.feature_extractors.ip2vec_extractor import Ip2VecExtractor
from custom_modules.feature_extractors.kitsune_feature_extractor import KitsuneFeatureExtractor


class FeatureExtractor:
    def __init__(self, selected_feature_extractors, selected_features, param):
        """
        :param selected_feature_extractors: feature extractors
        :param selected_features: selected features to apply feature extractors for each extractor
        :param param: parameters for models given as a dictionary of dictionaries
        """

        # all available feature extractors
        self.feature_extractors_map = {'autoencoder': Autoencoder,  # with preprocessed data
                                       'cluster_extractor': ClusterExtractor,  # with preprocessed data
                                       'ip2vec_extractor': Ip2VecExtractor,  # with raw data, batch learning
                                       'kitsune_feature_extractor': KitsuneFeatureExtractor,  # with raw data
                                       'lstm_autoencoder': LSTMAutoencoder,  # with preprocessed data
                                       'pca_extractor': PCAExtractor,  # with preprocessed data
                                       }

        self.selected_feature_extractors = selected_feature_extractors
        self.selected_features = selected_features
        self.param = param  # parameters for extractor models

        self.feature_extractors = self.create_extractors()

        self.features_extracted = {}

    def create_extractors(self):
        feature_extractors = {}
        for key in self.selected_feature_extractors:
            print(key)
            args = [self.param[key], self.selected_features[key]]
            feature_extractors[key] = self.feature_extractors_map[key](*args)

        return feature_extractors

    def fit(self, X):
        for key in self.feature_extractors.keys():
            self.feature_extractors[key].fit(X)

    def transform(self, X):
        for key in self.feature_extractors.keys():
            features_extracted = self.feature_extractors[key].transform(X)
            self.features_extracted[key] = features_extracted

        return self.features_extracted

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
