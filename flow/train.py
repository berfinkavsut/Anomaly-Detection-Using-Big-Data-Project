from pysad.transform.probability_calibration import ConformalProbabilityCalibrator
from models import Loda, XStream, IForest, KnnCad
from pysad.transform.ensemble.ensemblers import AverageScoreEnsembler
import numpy as np


class Train:
    def __init__(self, model_properties, ensemble_model_properties=None, thread=False):
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
        self.func_mapping = {
            'Loda': Loda,
            'xStream': XStream,
            'IForest': IForest,
            'KnnCad': KnnCad,
            # 'KitNet': KitNet,
        }
        self.models = {}  # Dictionary of models
        self.ensembler = AverageScoreEnsembler()
        # Generating models
        for model_key in model_properties:
            self.models[model_key] = self.create_model(model_key, model_properties[model_key])

        self.ensemble_models = {}  # Dictionary of ensemble models
        if ensemble_model_properties is not None:
            # Generating ensemble models
            for ens_key in ensemble_model_properties:

                inner_model_properties = ensemble_model_properties[ens_key]
                inner_models = {}  # Models in each ensemble are in this list
                for model_key in inner_model_properties:

                    if model_key in self.models.keys():
                        model = self.models[model_key]
                    else:
                        model = self.create_model(model_key, inner_model_properties[model_key])

                    inner_models[model_key] = model
                self.ensemble_models[ens_key] = inner_models

        #todo
        self.inc = 0
        self.thread = thread

        print(self.ensemble_models)
        self.ScoreConverter = ConformalProbabilityCalibrator()


    def create_model(self, model_key, model_properties):
        return self.func_mapping[model_key](**model_properties)

    def fit(self, X_train):


        if self.thread:
            return self.thread_fit(X_train)
        else:
            unique = self.get_unique_models()
            for model in unique.values():
                model.fit(X_train)
            return



    def predict(self, X_train):

        if X_train.ndim == 1:
            X_train = X_train.reshape(1, -1)

        pred = {}
        scs = {}
        ens_pred = {}

        for key in self.models:
            sc, pr = self.models[key].predict(X_train)
            pred[key] = pr
            scs[key] = sc

        for key in self.ensemble_models:

            i = 0
            scores = np.empty((X_train.shape[0], len(self.ensemble_models[key])))
            for model_key, model in self.ensemble_models[key].items():

                if model_key in self.models.keys():
                    if np.isnan(scs[model_key]):
                        a = 0
                    else:
                        a = scs[model_key]
                    scores[:, i] = a
                else:
                    scores[:, i] = model.predict(X_train)[0]

                i += 1

            ens_score = self.ensembler.fit_transform(scores)
            ens_pred[key] = self.ScoreConverter.fit_transform(ens_score)


        return pred, ens_pred

    def get_models(self):
        return self.models, self.ensemble_models



    def get_unique_models(self):

        unique = {}

        for key, model in self.models.items():
            if key not in unique.keys():
                unique[key] = model


        for key in self.ensemble_models:
            for model_key, model in self.ensemble_models[key].items():
                if model_key not in unique.keys():
                    unique[model_key] = model
        return unique


    #
    # def thread_fit(self, X_train):
    #
    #     s = time.time()
    #     unique = self.get_unique_models()
    #     print(time.time() - s)
    #     threads = []
    #
    #     for key, model in unique.items():
    #         threads.append(multiprocessing.Process(target=model.fit, args=(X_train, )))
    #
    #     s = time.time()
    #     for t in threads:
    #         t.start()
    #     print(time.time() - s)
    #     s = time.time()
    #     for t in threads:
    #         t.join()
    #     print(time.time() - s)
    #
    #
    #
    #
    #
    #
    #
    #
