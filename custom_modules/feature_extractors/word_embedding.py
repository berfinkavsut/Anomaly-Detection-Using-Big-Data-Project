from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor


class WordEmbedding(BaseFeatureExtractor):

    feature_extractor_name = 'word_embedding'

    def __init__(self, param, selected_features):
        super().__init__(param=param, selected_features=selected_features)

    def fit(self, X):
        pass

    def transform(self, X):
        pass

    def fit_transform(self, X):
        pass
