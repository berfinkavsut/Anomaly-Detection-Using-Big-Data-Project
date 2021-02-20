import numpy as np
from models import Loda, XStream, IForest



class Train:
    def __init__(self, num_features, model_properties, ensemble_model_properties=None):
        """
        :param num_features: Number of features.
        :param model_properties: Dictionary of dictionaries of model names and properties. Nested dictionaries contain
        model parameters.
        :param ensemble_model_properties: Dictionary of model properties for each ensemble.

        Example:
        model_properties = {'KitNet': {'key_A': 'value_A'},
                            'Loda': {'key_B': 'value_B'}}

        ensemble_model_properties = {'ens1': {'KitNet': {'key_A': 'value_A'}, 'Loda': {'key_B': 'value_B'}, 'xStream': {'key_B': 'value_B'}},
                                    'ens2': {'KitNet': {'key_A': 'value_A'}, 'xStream': {'key_B': 'value_B'}}}
        """
        self.num_features = num_features
        self.func_mapping = {
            'Loda': Loda,
            'xStream': XStream,
            'IForest': IForest,
            # 'KitNet': KitNet,
        }
        self.models = {}  # Dictionary of models
        # Generating models
        for model_key in model_properties:
            self.models[model_key] = self.create_model(model_key, model_properties[model_key])

        self.ensemble_models = {}  # Dictionary of ensemble models
        if ensemble_model_properties is not None:
            # Generating ensemble models
            for ens_key in ensemble_model_properties:
                inner_model_properties = ensemble_model_properties[ens_key]
                inner_models = []  # Models in each ensemble are in this list
                for model_key in inner_model_properties:
                    inner_models.append(self.create_model(model_key, inner_model_properties[model_key]))
                self.ensemble_models[ens_key] = inner_models



    def create_model(self, model_key, model_properties):
        return self.func_mapping[model_key](**model_properties)

    def fit(self, X_train):

        if X_train.ndim == 1:
            X_train = X_train.reshape(1, -1)

        for key in self.models:
            self.models[key].fit(X_train)

        for key in self.ensemble_models:
            for model in self.ensemble_models[key]:
                model.fit(X_train)
        return None

    def predict(self, X_train):

        if X_train.ndim == 1:
            X_train = X_train.reshape(1, -1)

        pred = {}
        ens_pred = {}
        for key in self.models:
            pred[key] = self.models[key].predict(X_train)[1]

        for key in self.ensemble_models:
            i = 0
            scores = np.empty((X_train.shape[0], len(self.ensemble_models[key])))
            for model in self.ensemble_models[key]:
                scores[:, i] = model.predict(X_train)[1]
                i += 1

            ens_pred[key] = np.mean(scores, axis=1)
            #ens_pred[key] = np.dot(scores, weights)

        return pred, ens_pred

    def get_models(self):
        return self.models, self.ensemble_models




