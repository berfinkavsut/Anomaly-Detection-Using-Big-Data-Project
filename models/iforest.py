"""
Implementation of iForest.
"""
from pysad.models.iforest_asd import IForestASD
from pysad.models.integrations import ReferenceWindowModel
from pysad.utils import ArrayStreamer
from pysad.evaluation import AUROCMetric
from pyod.models.iforest import IForest

from tqdm import tqdm



class iForest:
    def __init__(self, X_train):
        """

        """
        self.iterator = ArrayStreamer(shuffle=False)  # Init streamer to simulate streaming data.
        self.model=ReferenceWindowModel(model_cls=IForest, window_size=240, sliding_size=30, initial_window_X=X_train[:100])
        # self.model = IForestASD()

    def fit(self, X_train, y_train):
        """

        :param X_train:
        :param y_train:
        :return:
        """

        metric = AUROCMetric()  # Init area under receiver-operating-characteristics curve metric tracker.

        score_array_iforest = []

        for X, y in tqdm(self.iterator.iter(X_train, y_train)):  # (X_train[100:], Y_train[100:])

            self.model.fit_partial(X)  # Fit to the instance.
            score = self.model.score_partial(X)  # Score the instance.
            metric.update(y, score)  # Update the metric.

            score_array_iforest.append(score)
            print(score)
        # Output resulting AUROCS metric.
        print(metric.get())
        return metric.get(), score_array_iforest
