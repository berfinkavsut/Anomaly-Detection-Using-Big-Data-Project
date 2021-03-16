import time
from flow.system_flow import SystemFlow
from utils.animate_live import AnimateLive
import numpy as np
from elasticsearch import Elasticsearch
from datetime import datetime
from elasticsearch import Elasticsearch
import pandas as pd

props = {'xStream': {}, 'IForest': {}, 'Loda': {}}

ens_props = {'Ensemble (IForest and Loda)': {'IForest': {}, 'Loda': {}},
             'Ensemble (Loda and xStream)': {'Loda': {}, 'xStream': {}},
             'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}},}
data_dim = 10
#param is dictionary of dictionaries
param = {'autoencoder': {'latent_dim': data_dim,
                         'batch_size': 1,
                         'epoch_no': 5,
                         'optimizer': 'adam',
                         'loss': 'mse',
                         }
         }
col_names = [
        "time", "duration", "source_ip", "destination_ip", "protocol", "packet_len","dif_serv",
        "flag", "ip_vers", "src_port", "dst_port", "data_len", "seq", "seq_raw", "next_seq", "ack", "ack_raw",
        "flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push",
        "flags_reset", "flags_syn", "flags_fin", "win_size", "checksum", "checksum_status",
        "urgent_pointer", "proto_type", "proto_size", "hw_type", "hw_size", "hw_opcode", "src_hw_mac",
        "dst_hw_mac"
    ]
selected_features = {'autoencoder': col_names
                     }

selected_feature_extractors = ['autoencoder']

fe_config = {"selected_feature_extractors": selected_feature_extractors, "selected_features": selected_features, "param": param}
topic = "beste"
system_flow = SystemFlow(data_dim, props, ens_props, config="cloud", fe=True, fe_config=fe_config, verbose=True)

system_flow.create_stream(topic)
# anim = AnimateLive(ax_num=6, x_labels=["Time"] * 6, y_labels=["xStream", "IForest", "Loda", "Ensemble (IForest and Loda)",
#                                                     "Ensemble (Loda and xStream)", "Ensemble (xStream and IForest)"])

user = "elastic"
psw = "changeme"
access_url = f"http://{user}:{psw}@localhost:9200/"
es = Elasticsearch(hosts=access_url)

index = "test_flow"
es.indices.delete(index=index, ignore=[400, 404])

i = 0
while True:



    if i < 10:
        system_flow.fit_next(topic)
    else:
        s = time.time()
        probs, ens_probs, data = system_flow.fit_predict_next(topic)

        df1 = pd.DataFrame(data.reshape((1, -1)), columns=[f"C{i}" for i in range(len(data))])
        df2 = pd.DataFrame.from_dict(probs)
        df3 = pd.DataFrame.from_dict(ens_probs)
        df4 = pd.DataFrame.from_dict({"@timestamp": [datetime.utcnow()]})
        df = df1.join(df2.join(df3.join(df4)))
        data = df.to_dict('records')

        res = es.create(index=index, id=i+1, body=data[0])
        print(res['result'])

        es.indices.refresh(index=index)

        res = es.search(index=index, body={"query": {"match_all": {}}})
        print("Got %d Hits:" % res['hits']['total']['value'])

        time.sleep(1)








        # update_arr = np.array([])
        #
        # for key in probs.keys():
        #     update_arr = np.append(update_arr, probs[key])
        #
        # for key in ens_probs.keys():
        #     update_arr = np.append(update_arr, ens_probs[key])
        #
        # anim.update_data(update_arr, time.time()-s)
        # anim.update_graph()



    i+=1



