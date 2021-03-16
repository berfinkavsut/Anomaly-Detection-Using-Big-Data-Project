from custom_modules.feature_extractors.autoencoder import Autoencoder
from custom_modules.feature_extractors.basic_extractor import BasicExtractor
from custom_modules.feature_extractors.cluster_extractor import ClusterExtractor
from custom_modules.feature_extractors.lstm_autoencoder import LSTMAutoencoder
from custom_modules.feature_extractors.pca_extractor import PCAExtractor
from custom_modules.feature_extractors.tsfresh_extractor import TsFreshExtractor
from custom_modules.feature_extractors.word_embedding import WordEmbedding


class FeatureExtractor:
    def __init__(self, selected_feature_extractors, selected_features, param):
        """

        :param selected_features: selected features to apply feature extractors for each extractor
        :param param: parameters for models given as a dictionary of dictionaries
        :param sample_no: fixed sample number coming as batches
        """
        print(selected_feature_extractors)
        # all available feature extractors
        self.feature_extractors_map = {'autoencoder': Autoencoder,
                                       'basic_extractor': BasicExtractor,
                                       'cluster_extractor': ClusterExtractor,
                                       'lstm_autoencoder': LSTMAutoencoder,
                                       'pca_extractor': PCAExtractor,
                                       'tsfresh_extractor': TsFreshExtractor,
                                       'word_embedding': WordEmbedding,
                                       }

        self.selected_feature_extractors = selected_feature_extractors
        self.selected_features = selected_features
        self.param = param  # parameters for extractor models

        self.feature_extractors = self.create_extractors()

        #self.sample_no = sample_no  # seems that it is not used now ?
        self.features_extracted = {}

    def create_extractors(self):
        """

        :return:
        """

        feature_extractors = {}
        for key in self.selected_feature_extractors:
            print(key)
            args = [self.param[key], self.selected_features[key]]
            feature_extractors[key] = self.feature_extractors_map[key](*args)

        return feature_extractors

    def fit(self, X):
        """

        :param X:
        :return:
        """

        for key in self.feature_extractors.keys():
            self.feature_extractors[key].fit(X)

    def transform(self, X):
        """

        :param X:
        :return:
        """

        # self.features_extracted = {}  # inefficient?
        for key in self.feature_extractors.keys():
            features_extracted = self.feature_extractors[key].transform(X)
            self.features_extracted[key] = features_extracted

        return self.features_extracted

    def fit_transform(self, X):
        """

        :param X:
        :return:
        """

        self.fit(X)
        return self.transform(X)
