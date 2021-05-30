import pandas as pd

from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model

from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor


class Autoencoder(BaseFeatureExtractor):

    """
    NOTES
    Loss sometimes starts very large and cannot decay.
    """

    feature_extractor_name = 'autoencoder'

    def __init__(self, param, selected_features):
        """
        :param param: dictionary of parameters: latent_dim, batch_size, epoch_no, optimizer, loss
        :param selected_features: list of selected features
        """

        super().__init__(param=param, selected_features=selected_features)

        # for layer sizes
        self.latent_dim = self.param['latent_dim']
        self.n_features = len(self.selected_features)

        # training parameters
        self.batch_size = self.param['batch_size']
        self.epoch_no = self.param['epoch_no']
        self.optimizer = self.param['optimizer']  # 'adam' default optimizer
        self.loss = self.param['loss']  # 'mse' default loss function

        # define layers autoencoder model

        # 1D input
        self.input = Input(shape=(self.n_features,), name='input_encoder')
        self.encoder_layer = Dense(self.n_features,
                                   activation='relu',
                                   name='encoder')(self.input)
        self.bottleneck = Dense(self.latent_dim,
                                activation='tanh',
                                name='bottleneck')(self.encoder_layer)
        self.decoder_layer = Dense(self.n_features,
                                   activation='relu',
                                   name='decoder')(self.bottleneck)

        # define autoencoder model
        self.model = Model(inputs=self.input, outputs=self.decoder_layer)

        # compile model
        self.model.compile(optimizer=self.optimizer, loss=self.loss)

        # define encoder of the autoencoder which is the actual feature extractor
        self.encoder = Model(inputs=self.input, outputs=self.bottleneck)

    def fit(self, X):
        """
        Select a subset of X with respect to selected features before.
        Fit and train autoencoder model.

        :param X: data frame input
        :return:
        """

        X = X[self.selected_features]
        X = X.to_numpy()
        self.model.fit(x=X,
                       y=X,
                       batch_size=self.batch_size,
                       epochs=self.epoch_no,
                       verbose=0)

    def transform(self, X):
        """
        Select a subset of X with respect to selected features before.
        Reduce dimensionality of input with autoencoder.

        :param X: data frame input
        :return: data frame output of autoencoder
        """

        X = X[self.selected_features]
        X = X.to_numpy()
        self.features_extracted = self.encoder.predict(X)
        return self.features_extracted

    def fit_transform(self, X):
        """
        Select a subset of X with respect to selected features before.
        Fit and train autoencoder model.
        Reduce dimensionality of input with autoencoder.

        :param X: data frame input
        :return: data frame output of autoencoder
        """

        self.fit(X)
        self.features_extracted = self.transform(X)
        return self.features_extracted

    def get_model(self):
        """
        Get whole model of autoencoder for sanity check
        Model has encoder and decoder parts

        :return: autoencoder model
        """
        return self.model


