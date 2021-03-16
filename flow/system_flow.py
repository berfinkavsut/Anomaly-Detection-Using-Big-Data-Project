import pickle
from pathlib import Path
from flow import Train
from flow import DataConsumer
from transformers.network_data_transformer import network_data_transformer
from custom_modules.feature_extractor import FeatureExtractor
import pandas as pd
import numpy as np


class SystemFlow:

    def __init__(self, num_features, props, ens_props=None, config="cloud", fe=False, fe_config=None, verbose=True):

        self.train = Train(num_features=num_features, model_properties=props, ensemble_model_properties=ens_props)
        self.consumer = DataConsumer(config=config, verbose=verbose)
        self.streams = {}
        self.fe = fe

        if self.fe:
            self.extractor = FeatureExtractor(**fe_config)



    def train_extractor(self, topic, iteration=100):

        next_data = self.get_next(topic)
        self.data_columns = next_data

        for i in range(iteration):
            self.extractor.fit(next_data)


    def create_stream(self, topic):
        self.streams[topic] = self.consumer.stream_data(topic)


    def get_next(self, topic):

        data = next(self.streams[topic])
        transformed = network_data_transformer(data)

        if self.fe:
            result = self.extractor.fit_transform(transformed)['autoencoder'].to_numpy()
        else:
            result = transformed

        return result



    def fit_next(self, topic):
        next_data = self.get_next(topic)
        self.train.fit(next_data)
        return next_data

    def predict_next(self, topic):
        next_data = self.get_next(topic)
        return (*self.train.predict(next_data), next_data)

    def fit_predict_next(self, topic):
        next_data = self.get_next(topic)
        self.train.fit(next_data)
        return (*self.train.predict(next_data), next_data)

    def save_trained_models(self, path="saved_models"):
        models, ensemble_models = self.train.get_models()

        if models is not None:
            Path(f"{path}/models").mkdir(parents=True, exist_ok=True)
            for key in models.keys():
                with open(f"{path}/models/{key}", 'wb') as file:
                    pickle.dump(models[key], file)

        if ensemble_models is not None:
            Path(f"{path}/ensemble_models").mkdir(parents=True, exist_ok=True)
            for key in ensemble_models.keys():
                with open(f"{path}/ensemble_models/{key}", 'wb') as file:
                    pickle.dump(ensemble_models[key], file)
