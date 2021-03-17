from pysad.models import RobustRandomCutForest
from models.Detector import Detector


class RRCF(Detector):
    """
    iForest class which uses PyOD's iForest model to fit and predict streaming data
    """


    def __init__(self, num_trees=4, shingle_size=4, tree_size=256):
        """
        Initializes iterator which streams a given array, preprocessors and postprocessors, and the model itself
        """
        model = RobustRandomCutForest(num_trees, shingle_size, tree_size)
        # metric = AUROCMetric()
        lib = 'pysad'
        super().__init__(model, lib)


