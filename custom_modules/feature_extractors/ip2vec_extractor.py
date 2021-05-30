import pandas as pd
import torch as th
import numpy as np
import os

from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor

from custom_modules.feature_extractors.ip2vec import preprocess as p
from custom_modules.feature_extractors.ip2vec import trainer as t


class Ip2VecExtractor(BaseFeatureExtractor):

    feature_extractor_name = 'ip2vec_extractor'

    def __init__(self, param, selected_features):
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
        """
        :param X: data frame input
        :return: data frame output, subset of input
        """
        model = self.trainer_model.model
        embeddings = model.u_embedding.weight.detach().numpy()

        src_ips = X['source_ip'].to_numpy()
        dst_ips = X['destination_ip'].to_numpy()
        dst_ports = X['dst_port'].to_numpy()
        protocols = X['protocol_name'].to_numpy()

        src_ip_vectors = []
        dst_ip_vectors = []
        dst_port_vectors = []
        protocol_vectors = []

        for i in range(len(X)):

            src_ip = src_ips[i]
            ix = self.w2v[src_ip]
            src_ip_vector = embeddings[ix]
            src_ip_vectors.append(src_ip_vector)

            dst_ip = dst_ips[i]
            ix = self.w2v[dst_ip]
            dst_ip_vector = embeddings[ix]
            dst_ip_vectors.append(dst_ip_vector)

            dst_port = dst_ports[i]
            ix = self.w2v[dst_port]
            dst_port_vector = embeddings[ix]
            dst_port_vectors.append(dst_port_vector)

            protocol = protocols[i]
            ix = self.w2v[protocol]
            protocol_vector = embeddings[ix]
            protocol_vectors.append(protocol_vector)

        print(src_ip_vectors)
        print(dst_ip_vectors)
        print(dst_port_vectors)
        print(protocol_vectors)
        # self.features_extracted = ip_vectors

        return []

    def fit_transform(self, X):
        """
        :param X: data frame input
        :return: data frame output, subset of input
        """

        self.fit()
        self.features_extracted = self.transform(X)
        return self.features_extracted


os.chdir('..')
os.chdir('..')

main_dir = os.getcwd()
data_dir = os.path.join(main_dir, "data")
file_dir = os.path.join(data_dir, "Kitsune_45000_not_transformer.csv")
X = pd.read_csv(file_dir)
X = X.iloc[0:100, :]

selected_features = ['source_ip', 'destination_ip', 'dst_port', 'protocol_name']
X.dropna(subset=selected_features, inplace=True)

param = {'emb_dim': 32, 'max_epoch': 50, 'batch_size': 128, 'neg_num': 10}

ip2vec_extractor = Ip2VecExtractor(selected_features=selected_features, param=param)

ip2vec_extractor.fit(X)
features_extracted = ip2vec_extractor.transform(X)

# print(ip2vec_extractor.w2v)
# print(ip2vec_extractor.v2w)
print(features_extracted)

