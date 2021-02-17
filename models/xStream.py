from tqdm import tqdm
from pysad.utils import ArrayStreamer
from pysad.evaluation import AUROCMetric
from pysad.models import xStream as pysad_xStream
from pysad.transform.postprocessing import RunningAveragePostprocessor
from pysad.transform.preprocessing import InstanceUnitNormScaler
from models.Detector import Detector

class XStream(Detector):
    """
    xStream class which uses PySAD's xStream model to fit and predict streaming data
    """

    def __init__(self, window_size=5, shuffle=False):
        """
        Initializes iterator which streams a given array, preprocessors and postprocessors, and the model itself
        """
        model = pysad_xStream()  # Init model
        lib = 'pysad'
        super().__init__(model, lib)