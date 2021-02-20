from pysad.models import IForestASD
# from pyod.models.iforest import IForest as pyod_IForest
from tqdm import tqdm
from models.Detector import Detector


class IForest(Detector):
    """
    iForest class which uses PyOD's iForest model to fit and predict streaming data
    """


    def __init__(self, initial_window_X=None, window_size=2048):
        """
        Initializes iterator which streams a given array, preprocessors and postprocessors, and the model itself
        """
        model = IForestASD(initial_window_X=initial_window_X, window_size=window_size)
        # metric = AUROCMetric()
        lib = 'pysad'
        super().__init__(model, lib)


