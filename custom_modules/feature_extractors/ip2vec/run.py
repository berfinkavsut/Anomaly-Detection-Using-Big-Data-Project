import numpy as np
import pandas as pd

from custom_modules.feature_extractors.ip2vec import preprocess as p
from custom_modules.feature_extractors.ip2vec import trainer as t

# import ip2vec.preprocess as p
# import ip2vec.trainer as t
import torch as th
import os

batch_size = 1024

os.chdir('..')
os.chdir('..')
os.chdir('..')

main_dir = os.getcwd()
data_dir = os.path.join(main_dir, "data")
file_dir = os.path.join(data_dir, "Kitsune_45000_not_transformer.csv")
X = pd.read_csv(file_dir)

features = ['source_ip', 'destination_ip', 'dst_port', 'protocol_name']
X = X[features]
X.dropna(subset=features, inplace=True)
X = X.iloc[0:100, :]
# print(X.head(5))

d = X.to_numpy()
w2v, v2w = p._w2v(d)
print(w2v)
print(v2w)
corpus = pd.DataFrame(p._corpus(d, w2v)).to_numpy()
freq = p._frequency(d)
train = p._data_loader(corpus)
print('Train:', train)

device = th.device('cpu')
trainer_model = t.Trainer(w2v, v2w, freq, emb_dim=32, device=device)
trainer_model.fit(data=train, max_epoch=5, batch_size=256, neg_num=10)

model = trainer_model.model
# print(model.predict(train))

# th.save(model.state_dict(), 'ip2vec.pth')
# model_load = th.load("ip2vec.pth")

EMBEDDINGS = model.u_embedding.weight.detach().numpy()

# print('Most similar of 192.168.2.122:')
# trainer_model.most_similar('192.168.2.122', 5)

ip_address = X['source_ip']
ix = w2v[ip_address.values[0]]
print(len(w2v))
print('hey')
print(ix)
ip_vector = EMBEDDINGS[ix]
print(ip_vector.shape)
ip_vectors = []

for i in range(d.shape[0]):
    pkt = d[i]
    ip_address = pkt[0]
    ix = w2v[ip_address]
    ip_vector = EMBEDDINGS[ix]
    ip_vectors.append(ip_vector)

# print(ip_vectors)


