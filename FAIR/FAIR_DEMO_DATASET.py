import time

import numpy as np
import pandas as pd

from custom_modules.feature_extractors.ip2vec_extractor import Ip2VecExtractor
from flow.system_flow import SystemFlow
from utils.alert import Alert

props = {'xStream': {}, 'IForest': {}}
ens_props = {'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}}}



path_lstm = "../debug/Active_Wiretap_5000.csv" #dataset path
df_data_lstm = pd.read_csv(path_lstm)
X_train = df_data_lstm.loc[:, df_data_lstm.columns != 'label']
print(X_train)
dataset = X_train


data_dim = 10
# param is dictionary of dictionaries
param = {'autoencoder': {'latent_dim': data_dim,
                         'batch_size': 1,
                         'epoch_no': 5,
                         'optimizer': 'adam',
                         'loss': 'mse'}}

col_names = list(X_train.head(5))
print(col_names)

selected_features = {'autoencoder': col_names}
selected_feature_extractors = ['autoencoder']

fe_config = {"selected_feature_extractors": selected_feature_extractors, "selected_features": selected_features, "param": param}

selected_features = ['source_ip', 'destination_ip', 'dst_port', 'proto_type']

param = {'emb_dim': 10, 'max_epoch': 50, 'batch_size': 128, 'neg_num': 10}

ip2vec_extractor = Ip2VecExtractor(param=param, selected_features=selected_features)
fe_config = ip2vec_extractor


system_flow = SystemFlow(props, ens_props, config="cloud", fe=True, fe_config=fe_config, user="elastic",
                 psw="changeme", elk_index="test_flow", verbose=True, with_elastic=False, with_dataset=True, dataset=dataset)

thresholds = {'0.5': [0.5]}

i = 0

alarm = Alert()
while True:
    if i < 2:
        system_flow.fit_next()
        i += 1
    else:

        s = time.time()
        reduced_data, original_data, probs, ens_probs = system_flow.fit_predict_next()

        #Threshold and alert
        threshold = system_flow.return_threshold()

        probsarray = []
        for key in probs:
            probsarray.append(probs[key][0])

        for key in ens_probs:
            probsarray.append(ens_probs[key][0])

        max_prob = max(probsarray)
        print("maxprob" , max_prob)

        if threshold < max_prob:
            alarm.send_email()

        thresholds = {'threshold': [threshold]}

        # Send to elastic
        system_flow.send_to_elk(original_data, probs, ens_probs, thresholds)


        # # Update hyperparameters
        # hyperparameters = system_flow.return_hyperparameter()
        #
        # if old_hyp != hyperparameters:
        #     system_flow.update(hyperparameters)
        #
        # old_hyp = hyperparameters

