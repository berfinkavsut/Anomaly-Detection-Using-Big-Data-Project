"""
Implementation of LODA from PyOD.
"""
# from pyod.models.loda import LODA
from models.Detector import Detector
from pysad.models import LODA


class Loda(Detector):
    def __init__(self, num_bins=10, num_random_cuts=100):
        model = LODA(num_bins=num_bins, num_random_cuts=num_random_cuts)
        lib = 'pysad'
        super().__init__(model, lib)
