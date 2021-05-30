import pandas as pd
import numpy as np
import os

from custom_modules.feature_extractors.lstm_autoencoder import LSTMAutoencoder
from sklearn.metrics import mean_squared_error

os.chdir('..')

main_dir = os.getcwd()
data_dir = os.path.join(main_dir, "data")
file_dir = os.path.join(data_dir, "sample_train.csv")
data = pd.read_csv(file_dir, header=None)

data = pd.DataFrame.to_numpy(data)
data = data[1::]
data = np.nan_to_num(data)
data = pd.DataFrame(data)
features = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes',
            'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
            'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
            'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
            'num_access_files', 'num_outbound_cmds', 'is_host_login',
            ]
data.columns = features
# data = data[0:32]
X = data
selected_features = features

param = {'latent_dim': 10,
         'time_step': 1,  # will be fixed
         'epoch_no': 5,
         'optimizer': 'adam',
         'loss': 'mse',
         }

lstm_autoencoder = LSTMAutoencoder(param=param, selected_features=selected_features)
lstm_autoencoder.fit(X)
extracted_features = lstm_autoencoder.transform(X)
extracted_features2 = lstm_autoencoder.transform(X)

model = lstm_autoencoder.get_model()
X_test = data[selected_features]
X_test1 = X_test.to_numpy()
X_test = X_test1.reshape(X_test1.shape[0], 1, X_test1.shape[1])
# X = pd.DataFrame(X)
X_hat = model.predict(X_test)

print(X_test.shape)
print(X_hat.shape)
print('checkpoint')
X_hat = X_hat.reshape(X_hat.shape[0], -1)
score = mean_squared_error(X_test1, X_hat)
print('MSE:', score)

