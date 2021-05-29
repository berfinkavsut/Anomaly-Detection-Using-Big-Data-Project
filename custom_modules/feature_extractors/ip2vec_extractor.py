import pandas as pd
import torch as th
import numpy as np

from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor

from custom_modules.feature_extractors.ip2vec import preprocess as p
from custom_modules.feature_extractors.ip2vec import trainer as t


class Ip2VecExtractor(BaseFeatureExtractor):

    feature_extractor_name = 'ip2vec_extractor'

    def __init__(self, param, selected_features, dataset):
        """
        :param param: dictionary for model parameters
        :param selected_features: selected features to extract features
        """

        super().__init__(param=param, selected_features=selected_features)

        # parameters
        self.emb_dim = self.param['emb_dim']
        self.max_epoch = self.param['max_epoch']
        self.batch_size = self.param['batch_size']
        self.neg_num = self.param['neg_num']

        # take categorical features
        self.features = ['source_ip', 'destination_ip', 'dst_port', 'protocol_name']
        X = dataset[self.features]
        self.d = X.to_numpy()

        self.w2v, self.v2w = p._w2v(self.d)
        self.corpus = pd.DataFrame(p._corpus(self.d, self.w2v)).to_numpy()
        self.freq = p._frequency(self.d)
        self.batch_size = 1#?
        self.train = p._data_loader(self.corpus, self.batch_size)
        self.trainer_model = t.Trainer(self.w2v, self.v2w, self.freq, emb_dim=32, device=th.device('cpu'))

    def fit(self, X):
        self.trainer_model.fit(data=self.train, max_epoch=5, batch_size=256, neg_num=10)

    def transform(self, X):
        """
        :param X: data frame input
        :return: data frame output, subset of input
        """
        model = self.trainer_model.model
        embeddings = model.u_embedding.weight.detach().numpy()

        # print('Most similar of 192.168.2.122:')
        # trainer_model.most_similar('192.168.2.122', 5)

        features = ['source_ip', 'destination_ip', 'dst_port', 'protocol_name']

        ip_addresses = X['source_ip']
        ix = self.w2v[ip_addresses]
        ip_vector = embeddings[ix]
        print(ip_vector.shape)
        ip_vectors = []

        for i in range(d.shape[0]):
            pkt = d[i]
            ip_address = pkt[0]
            ix = w2v[ip_address]
            ip_vector = EMBEDDINGS[ix]
            ip_vectors.append(ip_vector)

        print(ip_vectors)


        self.features_extracted = X[self.selected_features]
        return self.features_extracted

    def fit_transform(self, X):
        """
        :param X: data frame input
        :return: data frame output, subset of input
        """

        self.fit(X)
        self.features_extracted = self.transform(X)
        return self.features_extracted
