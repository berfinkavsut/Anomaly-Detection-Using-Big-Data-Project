
from tqdm import tqdm
# import mmh3
from pysad.models.integrations import ReferenceWindowModel
from pysad.utils import ArrayStreamer
from pysad.evaluation import AUROCMetric
from pysad.models import xStream
from pysad.transform.postprocessing import RunningAveragePostprocessor
from pysad.transform.preprocessing import InstanceUnitNormScaler


class xstream:

    def __init__(self, X):
        self.iterator = ArrayStreamer(shuffle=False)  # Init streamer to simulate streaming data.
        self.preprocessor = InstanceUnitNormScaler()  # Init normalizer.
        self.postprocessor = RunningAveragePostprocessor(window_size=5)  #
        self.model = xStream()
        self.metric = AUROCMetric()

    def fit(self, X, Y):
        iterator = self.iterator
        model = self.model
        preprocessor = self.preprocessor
        postprocessor = self.postprocessor
        metric = self.metric

        scores = []

        for x, y in tqdm(iterator.iter(X, Y)):  # Stream data.
            x = preprocessor.fit_transform_partial(x)
            score = model.fit_score_partial(x)  # Score the instance.
            score = postprocessor.fit_transform_partial(score)
            metric.update(y, score)  # Update the metric.

            scores.append(score[0])

        return metric.get(), scores

    def predict(self, X, Y=None):
        iterator = self.iterator
        model = self.model
        preprocessor = self.preprocessor
        postprocessor = self.postprocessor
        metric = self.metric
        scores = []

        for x, y in tqdm(iterator.iter(X,  Y)):  # Stream data.
            x = preprocessor.fit_transform_partial(x)
            score = model.score_partial(x)  # Score the instance.
            score = postprocessor.fit_transform_partial(score)
            metric.update(y, score)  # Update the metric.

            scores.append(score[0])

        return metric.get(), scores
