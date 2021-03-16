import pickle
from pathlib import Path
from flow import Train
from flow import DataConsumer
from transformers.network_data_transformer import network_data_transformer


class SystemFlow:

    def __init__(self, num_features, props, ens_props=None, config = "cloud", verbose=True):
        self.train = Train(num_features=num_features, model_properties=props, ensemble_model_properties=ens_props)
        self.consumer = DataConsumer(config=config, verbose=verbose)
        self.streams = {}

    def create_stream(self, topic):
        self.streams[topic] = self.consumer.stream_data(topic)

    def get_next(self, topic):
        data = next(self.streams[topic])[0]
        return network_data_transformer(data)

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
