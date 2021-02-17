"""
Implementation of LODA from PyOD.
"""
from pyod.models.loda import LODA
from models.Detector import Detector


class Loda(Detector):
    def __init__(self, contamination=0.1, n_bins=10, n_random_cuts=100):
        model = LODA(contamination, n_bins, n_random_cuts)
        lib = 'pyod'
        super().__init__(model, lib)
