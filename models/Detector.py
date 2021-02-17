
from pysad.transform.probability_calibration import ConformalProbabilityCalibrator
from pysad.transform.probability_calibration import GaussianTailProbabilityCalibrator

class Detector:
    """
    iForest class which uses PyOD's iForest model to fit and predict streaming data
    """


    def __init__(self, model, lib=None, metric=None, iterator=None):
        """
        Initializes iterator which streams a given array, preprocessors and postprocessors, and the model itself
        """
        self.model = model
        self.metric = metric
        self.iterator = iterator
        self.lib = lib

        if lib == 'pysad':
            self.ScoreConverter = ConformalProbabilityCalibrator()


    def fit(self, X):
        """

        :param X:
        :return:
        """

        self.model = self.model.fit(X)


    def predict(self, X):
        """
        Predict the data without fitting.
        :param X: Data to be predicted.
        :return: scores, probs: Anomaly scores, probability for anomaly.
        """

        if self.lib == 'pyod':
            scores = self.model.decision_function(X)
            probs = self.model.predict_proba(X)[:,1]
        elif self.lib == 'pysad':
            scores = self.model.score(X)
            probs = (scores - scores.min())/(scores.max() - scores.min()) #self.ScoreConverter.fit_transform(scores)
        else:
            raise Exception("Model not defined!")

        return scores, probs


    def fit_predict(self, X):
        """
        Fit and predict the data.
        :param X: Data to be used.
        :return: scores, probs: Anomaly scores, probability for anomaly.
        """
        self.fit(X)
        return self.predict(X)


    #
    # def update_AUROC(self, score, Y=None):
    #     if Y is not None:
    #         self.metric.update(Y, score)
    #
    # def get_AUROC(self):
    #     return self.metric.get()

