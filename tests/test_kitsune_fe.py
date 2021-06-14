import pandas as pd
import numpy as np

import os

from custom_modules.feature_extractors.kitsune_feature_extractor import KitsuneFeatureExtractor

os.chdir('..')

main_dir = os.getcwd()
data_dir = os.path.join(main_dir, "data")
path = os.path.join(data_dir, "Kitsune_45000_not_transformer.csv")

data = pd.read_csv(path)
columns = data.columns
data = pd.DataFrame.to_numpy(data)
data = np.nan_to_num(data)
data = pd.DataFrame(data)
data.columns = columns

# packet_limit = np.Inf  # the number of packets to process
packet_limit = len(data)

param = {'limit': packet_limit,  # or np.inf
         'Lambdas': np.nan,
         'HostLimit': 100000000000,
         'HostSimplexLimit': 100000000000}

selected_features = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes',
                     'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
                     'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
                     'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
                     'num_access_files', 'num_outbound_cmds', 'is_host_login',
                     ]

kitsune_fe = KitsuneFeatureExtractor(param=param, selected_features=selected_features)
kitsune_fe.fit()

for i in range(10):
    pkt = data.iloc[i]
    features_extracted = kitsune_fe.transform(pkt)
    print(features_extracted)