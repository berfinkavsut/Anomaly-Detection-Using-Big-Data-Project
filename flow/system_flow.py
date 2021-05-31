import pickle
from pathlib import Path
import pytz
from flow import Train
from flow import DataConsumer
from transformers.network_data_transformer import network_data_transformer
from custom_modules.feature_extractor import FeatureExtractor
import pandas as pd
from elasticsearch import Elasticsearch
from datetime import datetime, timezone
import numpy as np
import pandas as pd


class SystemFlow:

    def __init__(self, num_features, props, ens_props=None, config="cloud", fe=False, fe_config=None, user="elastic",
                 psw="changeme", elk_index="test_flow", verbose=True):

        self.train = Train(model_properties=props, ensemble_model_properties=ens_props)

        self.consumer = DataConsumer(config=config, verbose=verbose)

        access_url = f"http://{user}:{psw}@localhost:9200/"
        self.es = Elasticsearch(hosts=access_url)
        self.es.indices.delete(index=elk_index, ignore=[400, 404])
        self.elk_index = elk_index

        self.streams = {}

        self.fe = fe
        if self.fe:
            self.extractor = FeatureExtractor(**fe_config)
            self.extractor_trained = False



    def update(self, hyp):
        self.train = Train



    def return_hyperparameter(self):
        body = {
            "query": {
                "terms": {
                    "_id": ["1"]
                }
            }
        }
        searchRes = self.es.search(index="hyperparameters", body=body)
        return searchRes['hits']['hits'][0]["_source"]

    def return_threshold(self):
        body = {
            "query": {
                "terms": {
                    "_id": ["1"]
                }
            }
        }
        searchRes = self.es.search(index="thresholds", body=body)
        return searchRes['hits']['hits'][0]["_source"]["threshold"]



    def create_stream(self, topic):
        self.streams[topic] = self.consumer.stream_data(topic)




    def get_next(self, topic):

        original_data = next(self.streams[topic])
        transformed = network_data_transformer(original_data)

        if self.fe:

            result = self.extractor.fit_transform(transformed)['autoencoder'].to_numpy()

        else:
            result = transformed

        return result, original_data



    def fit_next(self, topic):
        next_data, original_data = self.get_next(topic)

        self.train.fit(next_data)
        return next_data, original_data




    def predict_next(self, topic):
        next_data, original_data = self.get_next(topic)

        self.send_to_elk(original_data, *self.train.predict(next_data))

        return (next_data, original_data, *self.train.predict(next_data))




    def fit_predict_next(self, topic):
        next_data, original_data = self.get_next(topic)
        self.train.fit(next_data)
        return (next_data, original_data, *self.train.predict(next_data))



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



    def send_to_elk(self, original_data, probs, ens_probs, thresholds):

        timestamp = datetime.strptime(original_data.at[0, "date&time"], '%Y-%m-%d %H:%M:%S.%f').astimezone(pytz.utc)
        timestamp = datetime.utcnow()
        thresholds_df = pd.DataFrame(data=thresholds)


        probs_df = pd.DataFrame.from_dict(probs)
        ens_probs_df = pd.DataFrame.from_dict(ens_probs)
        timestamp_df = pd.DataFrame.from_dict({"@timestamp": [timestamp]})

        #df = original_data.join(probs_df.join(ens_probs_df.join(timestamp_df)))
        df = original_data.join(probs_df.join(ens_probs_df.join(thresholds_df.join(timestamp_df))))

        data = df.to_dict('records')



        res = self.es.create(index=self.elk_index, id=datetime.utcnow(), body=data[0])
        print(res['result'])

        self.es.indices.refresh(index=self.elk_index)

        res = self.es.search(index=self.elk_index, body={"query": {"match_all": {}}})
        print("Got %d Hits:" % res['hits']['total']['value'])
