import time
from flow.system_flow import SystemFlow
from utils.animate_live import AnimateLive
import numpy as np

data_dim = 9

props = {'xStream': {}, 'IForest': {}, 'Loda': {}}

ens_props = {'Ensemble (IForest and Loda)': {'IForest': {}, 'Loda': {}},
             'Ensemble (Loda and xStream)': {'Loda': {}, 'xStream': {}},
             'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}},}

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

selected_features = {'autoencoder': col_names}
selected_feature_extractors = ['autoencoder']

fe_config = {"selected_feature_extractors": selected_feature_extractors, "selected_features": selected_features, "param": param}
system_flow = SystemFlow(data_dim, props, ens_props, config="cloud", fe=True, fe_config=fe_config, verbose=True)
topic = "beste"
system_flow.create_stream(topic)
#system_flow.train_extractor(topic, iteration=100)#
anim = AnimateLive(ax_num=6, x_labels=["Time"] * 6, y_labels=["xStream", "IForest", "Loda", "Ensemble (IForest and Loda)",
                                                    "Ensemble (Loda and xStream)", "Ensemble (xStream and IForest)"])
i = 0
train_iter = 20
while True:

    if i < train_iter:
        system_flow.fit_next(topic)
        i += 1
    else:
        s = time.time()
        probs, ens_probs, data = system_flow.fit_predict_next(topic)
        print(probs, ens_probs, data)

        update_arr = np.array([])

        for key in probs.keys():
            update_arr = np.append(update_arr, probs[key])

        for key in ens_probs.keys():
            update_arr = np.append(update_arr, ens_probs[key])

        anim.update_data(update_arr, time.time()-s)
        anim.update_graph()
