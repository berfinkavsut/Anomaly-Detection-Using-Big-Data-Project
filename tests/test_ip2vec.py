import pandas as pd
import os

from custom_modules.feature_extractors.ip2vec_extractor import Ip2VecExtractor

os.chdir('..')

main_dir = os.getcwd()
data_dir = os.path.join(main_dir, "data")
file_dir = os.path.join(data_dir, "Kitsune_45000_not_transformer.csv")
X = pd.read_csv(file_dir)
X = X.iloc[0:5, :]

selected_features = ['source_ip', 'destination_ip', 'dst_port', 'protocol_name']
X.dropna(subset=selected_features, inplace=True)

param = {'emb_dim': 10, 'max_epoch': 50, 'batch_size': 128, 'neg_num': 10}

ip2vec_extractor = Ip2VecExtractor(selected_features=selected_features, param=param)

ip2vec_extractor.fit(X)
features_extracted = ip2vec_extractor.transform(X)

print(features_extracted)
