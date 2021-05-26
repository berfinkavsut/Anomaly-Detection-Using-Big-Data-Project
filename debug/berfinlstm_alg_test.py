import pandas as pd
from AD131AMSTERDAM import DEBUG
import numpy as np
from sklearn.metrics import confusion_matrix
import time

from sklearn import preprocessing


props = {'xStream': {}, 'IForest': {}, 'Loda': {}}

ens_props = {'Ensemble (IForest and Loda)': {'IForest': {}, 'Loda': {}},
             'Ensemble (Loda and xStream)': {'Loda': {}, 'xStream': {}},
             'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}}
             }


# props = {'xStream': {}, 'IForest': {}}
#
# ens_props = {
#              'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}}
#              }

# a = 38000 - 3800
# b = a + 1000
# c = a - 10000

c = 5000
b = 15000

data_cic = pd.read_csv('lstm-autoencoder-dim10-label.csv')


labels = data_cic.iloc[c:b,-1:]
Y = labels.to_numpy()

data = data_cic.iloc[c:b, 0:-1]
X = data.to_numpy()

print(X.shape)
print(Y.shape)
print(np.mean(Y))
# df = pd.read_csv('Mirai_dataset.csv')[cut1:cut]
#
# idx = np.random.permutation(df.index)
#
#
# arr = df.to_numpy()
# arr = df.reindex(idx).to_numpy()
#
# # scaler = preprocessing.MinMaxScaler()
# # arr = scaler.fit_transform(arr)
# X = arr
# print("x", X)
#
# df_label = pd.read_csv('Mirai_labels.csv')[cut1:cut]
# arr_label = df_label.reindex(idx).to_numpy()
# arr_label = df_label.to_numpy()
# Y = arr_label.astype("int")
# print(Y)
# print(np.mean(Y))





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




db = DEBUG(props=props, ens_props=ens_props, fe_config=fe_config, fe=False)


y_pred = {}
for key in ens_props:
    y_pred[key] = np.empty((Y.shape[0]))

for key in props:
    y_pred[key] = np.empty((Y.shape[0]))

t1 = time.time()
i = 0
for data, lbl in zip(X, Y):
    data = data.reshape(1, -1)
    pred = db.fit_predict_next(data)


    for key in pred[0]:
        y_pred[key][i] = pred[0][key][0]

    for key in pred[1]:
        y_pred[key][i] = pred[1][key][0]

    db.updateAUROC(int(lbl), pred)
    i += 1
    if i % 100 == 0:
        print(i)
        print(pred)

        t2 = time.time()
        print(t2 - t1)

db.getAUROC()

threshold = 0.85
print("thrs", threshold)
for key in y_pred:
    print(confusion_matrix(Y, (y_pred[key] > threshold) * 1))

threshold = 0.65
print("thrs", threshold)
for key in y_pred:
    print(confusion_matrix(Y, (y_pred[key] > threshold) * 1))

threshold = 0.55
print("thrs", threshold)
for key in y_pred:
    print(confusion_matrix(Y, (y_pred[key] > threshold) * 1))

threshold = 0.75
print("thrs", threshold)
for key in y_pred:
    print(confusion_matrix(Y, (y_pred[key] > threshold) * 1))