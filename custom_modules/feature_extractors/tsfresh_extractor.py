import pandas as pd

from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model

from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor


class TsFreshExtractor(BaseFeatureExtractor):

    """
    NOTES
    Loss sometimes starts very large and cannot decay.
    """

    feature_extractor_name = 'tsfresh_extractor'

    def __init__(self):
        pass

    def fit(self, X):
        pass

    def transform(self, X):
        pass

    def fit_transform(self, X):
        pass

