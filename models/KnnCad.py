from pysad.models import KNNCAD
from models.Detector import Detector

class KnnCad(Detector):
    """
    KNNCAD
    """


    def __init__(self, probationary_period=100):
        """
        Initializes iterator which streams a given array, preprocessors and postprocessors, and the model itself
        """
        model = KNNCAD(probationary_period=probationary_period)
        lib = 'pysad'
        super().__init__(model, lib)