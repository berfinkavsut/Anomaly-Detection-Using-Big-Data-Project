import pandas as pd
import torch as th
import numpy as np

from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor
from custom_modules.feature_extractors.ip2vec import preprocess as p
from custom_modules.feature_extractors.ip2vec import trainer as t


class Ip2VecExtractor(BaseFeatureExtractor):
    """
    Notes:
    Works with raw data!
    Not compatible with online learning right now!
    """
    feature_extractor_name = 'ip2vec_extractor'

    def __init__(self, param, selected_features):

        super().__init__(param=param, selected_features=selected_features)

        # parameters
        self.emb_dim = self.param['emb_dim']
        self.max_epoch = self.param['max_epoch']
        self.batch_size = self.param['batch_size']
        self.neg_num = self.param['neg_num']

        # take categorical features
        self.features = selected_features

        self.w2v = []
        self.v2w = []
        self.corpus = []
        self.freq = []
        self.d = []

        self.trainer_model = []
        self.train = []

    def fit(self, X):

        X = X[self.features]
        self.d = X.to_numpy()

        self.w2v, self.v2w = p._w2v(self.d)
        self.corpus = pd.DataFrame(p._corpus(self.d, self.w2v)).to_numpy()
        self.freq = p._frequency(self.d)

        self.train = p._data_loader(self.corpus)
        self.trainer_model = t.Trainer(self.w2v, self.v2w, self.freq, emb_dim=self.emb_dim, device=th.device('cpu'))
        self.trainer_model.fit(data=self.train,
                               max_epoch=self.max_epoch,
                               batch_size=self.batch_size,
                               neg_num=self.neg_num)

    def transform(self, X):

        model = self.trainer_model.model
        embeddings = model.u_embedding.weight.detach().numpy()

        X = X[self.features].to_numpy()
        feature_vectors = []

        for i in range(X.shape[0]):
            print(i)
            pkt = X[i]
            feature_vector = np.array([])
            for j in range(X.shape[1]):
                feature = pkt[j]
                ix = self.w2v[feature]
                new_vector = embeddings[ix]
                feature_vector = np.concatenate((feature_vector, new_vector), axis=0)
            feature_vectors.append(feature_vector)

        self.features_extracted = np.array(feature_vectors)

        return self.features_extracted

    def fit_transform(self, X):

        self.fit(X)
        self.features_extracted = self.transform(X)
        return self.features_extracted