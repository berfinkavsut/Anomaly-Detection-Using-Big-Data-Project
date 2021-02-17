from pysad.models.integrations import ReferenceWindowModel
from pysad.utils import ArrayStreamer
from pysad.evaluation import AUROCMetric
from pyod.models.iforest import IForest as pyod_IForest
from tqdm import tqdm
from models.Detector import Detector


class IForest(Detector):
    """
    iForest class which uses PyOD's iForest model to fit and predict streaming data
    """


    def __init__(self, n_estimators=100, contamination=0.1):
        """
        Initializes iterator which streams a given array, preprocessors and postprocessors, and the model itself
        """
        model = pyod_IForest(n_estimators=n_estimators,
                             max_samples="auto",
                             contamination=contamination,
                             max_features=1.,
                             bootstrap=False,
                             n_jobs=1,
                             behaviour='old',
                             random_state=None,
                             verbose=0)
        # metric = AUROCMetric()
        lib = 'pyod'
        super().__init__(model, lib)


