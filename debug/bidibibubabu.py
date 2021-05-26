import pandas as pd
from sklearn.preprocessing import StandardScaler

from AD131AMSTERDAM import DEBUG
import numpy as np


props = {'xStream': {}, 'IForest': {}, 'Loda': {}}

ens_props = {'Ensemble (IForest and Loda)': {'IForest': {}, 'Loda': {}},
             'Ensemble (Loda and xStream)': {'Loda': {}, 'xStream': {}},
             'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}}
             }
### For cic
data_cic = pd.read_csv('Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')
data_cic=data_cic[~data_cic.isin([np.nan, np.inf, -np.inf]).any(1)]
data_cic=data_cic.dropna()
data_cic=data_cic.fillna(data_cic.median())
labels_cic=data_cic.iloc[:,-1:]
labels_cic=labels_cic.to_numpy()

data_cic=data_cic.to_numpy()
data_cic=data_cic[ : , 0:-1]
labels_cic=np.where(labels_cic=='BENIGN', 0, labels_cic)
Y=np.where(labels_cic=='DDoS', 1, labels_cic)
data_cic = data_cic.astype(np.float)
X = StandardScaler().fit_transform(data_cic)

print(np.where(Y == 1))

Y = Y[18500:19000]
X = X[18500:19000]

print(Y.sum(), Y.shape, X.shape)


####### For datasets
# df = pd.read_csv('')
# print(df)
#
# arr = df.to_numpy()
# X = arr[:, 1:-1]
# Y = arr[:, -1].astype("int")



print(X.shape, Y.shape)

data_dim = 20

param = {
        'autoencoder':
             {'latent_dim': data_dim,
             'batch_size': 1,
             'epoch_no': 5,
             'optimizer': 'adam',
             'loss': 'mse',}
         }
col_names = [ "duration", "source_ip", "destination_ip", "protocol", "packet_len","dif_serv",
            "flag", "ip_vers", "src_port", "dst_port", "data_len", "seq", "seq_raw", "next_seq", "ack", "ack_raw",
            "flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push",
            "flags_reset", "flags_syn", "flags_fin", "win_size", "checksum", "checksum_status",
            "urgent_pointer", "proto_type", "proto_size", "hw_type", "hw_size", "hw_opcode", "src_hw_mac",
            "dst_hw_mac"]
selected_features = {'autoencoder': col_names}

selected_feature_extractors = ['autoencoder']

fe_config = {"selected_feature_extractors": selected_feature_extractors, "selected_features": selected_features, "param": param}




db = DEBUG(props=props, ens_props=ens_props, fe_config=None, fe=False)


i = 0
for data, lbl in zip(X, Y):
    data = data.reshape(1, -1)
    pred = db.fit_predict_next(data)
    db.updateAUROC(int(lbl), pred)
    i += 1

db.getAUROC()
