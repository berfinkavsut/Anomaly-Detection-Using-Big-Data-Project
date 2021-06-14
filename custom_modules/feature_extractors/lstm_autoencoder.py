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
    """
    Notes:
    Works with preprocessed data!
    """

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
        self.optimizer = self.param['optimizer']
        self.loss = self.param['loss']

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

        X = X[self.selected_features]
        X = X.to_numpy()

        # reshape inputs for LSTM [samples, time_steps, features]
        X = X.reshape(X.shape[0], 1, X.shape[1])

        features_extracted = self.lstm_autoencoder.predict(X)
        features_extracted = pd.DataFrame(features_extracted)

        return features_extracted

    def fit_transform(self, X):

        self.fit(X)
        features_extracted = self.transform(X)
        return features_extracted

    def get_model(self):
        return self.model