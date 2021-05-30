# numpy==1.19.2

import pandas as pd

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import RepeatVector
from tensorflow.keras.layers import TimeDistributed

from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor


class LSTMAutoencoder(BaseFeatureExtractor):
    feature_extractor_name = 'lstm_autoencoder'

    def __init__(self, param, selected_features):
        super().__init__(param=param, selected_features=selected_features)

        self.model = []  # for feature extraction model
        self.param = param  # for model parameters

        # selected columns of data frame for feature extraction
        self.selected_features = selected_features

        self.latent_dim = self.param['latent_dim']
        # self.time_step = self.param['time_step']
        self.time_step = 1
        self.n_features = len(selected_features)

        # training parameters
        self.epoch_no = self.param['epoch_no']
        self.optimizer = self.param['optimizer']  # 'adam' default ?
        self.loss = self.param['loss']  # 'mse' default ?

        # LSTM auto encoder

        # encoder part
        self.input = Input(shape=(self.time_step, self.n_features), name='input')
        self.encoder_layer = LSTM(units=self.latent_dim,
                                  activation='relu',
                                  name='encoder_layer')(self.input)

        # decoder part
        self.repeat_layer = RepeatVector(self.time_step,
                                         name='repeat_vector')(self.encoder_layer)  # bridge between encoder and decoder
        self.decoder_layer = LSTM(units=self.latent_dim,
                                  activation='relu',
                                  return_sequences=True,
                                  name='lstm')(self.repeat_layer)

        self.output_layer = TimeDistributed(Dense(self.n_features))(self.decoder_layer)

        # create model
        self.model = Model(inputs=self.input, outputs=self.output_layer)
        self.model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

        # define encoder of the LSTM auto encoder which is the actual feature extractor
        self.lstm_autoencoder = Model(inputs=self.input, outputs=self.encoder_layer)

        # self.model.summary()
        # self.lstm_autoencoder.summary()

    def fit(self, X):
        """

        :param X:
        :return:
        """

        X = X[self.selected_features]
        X = X.to_numpy()

        # reshape inputs for LSTM [samples, time_steps, features]
        X = X.reshape(X.shape[0], 1, X.shape[1])

        history = self.model.fit(x=X,
                                 y=X,
                                 epochs=self.epoch_no,
                                 validation_split=0.15,
                                 verbose=1,
                                 ).history
        return history

    def transform(self, X):
        """

        :param X:
        :return:
        """

        X = X[self.selected_features]
        X = X.to_numpy()

        # reshape inputs for LSTM [samples, time_steps, features]
        X = X.reshape(X.shape[0], 1, X.shape[1])

        features_extracted = self.lstm_autoencoder.predict(X)
        features_extracted = pd.DataFrame(features_extracted)

        return features_extracted

    def fit_transform(self, X):
        """

        :param X:
        :return:
        """
        self.fit(X)
        features_extracted = self.transform(X)
        return features_extracted

    def get_model(self):
        return self.model

"""
import pandas as pd
import numpy as np
import os

from sklearn.metrics import mean_squared_error

os.chdir('..')
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
"""
