import pickle
from pathlib import Path
from flow import Train
from flow import DataConsumer
from transformers.network_data_transformer import network_data_transformer
from custom_modules.feature_extractor import FeatureExtractor
import pandas as pd


class SystemFlow:

    def __init__(self, num_features, props, ens_props=None, config="cloud", fe=False, fe_config=None, verbose=True):
        self.train = Train(num_features=num_features, model_properties=props, ensemble_model_properties=ens_props)
        self.consumer = DataConsumer(config=config, verbose=verbose)
        self.streams = {}
        self.fe = fe
        if fe:
            self.extractor = FeatureExtractor(**fe_config)

    def create_stream(self, topic):
        self.streams[topic] = self.consumer.stream_data(topic)

    def get_next(self, topic):
        data = next(self.streams[topic])
        #todo:
        df = pd.DataFrame(data.reshape(1, -1), columns=["a", "b", "d", "a2", "b2", "d2", "a3", "b3", "d3"])
        print(df)
        #transformed = data
        #transformed = network_data_transformer(data)
        if self.fe:
            a = self.extractor.fit_transform(df)
            print(a)
            return a
        #return transformed

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
