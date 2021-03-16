from tsfresh.examples.robot_execution_failures import download_robot_execution_failures
from tsfresh.examples.robot_execution_failures import load_robot_execution_failures
from tsfresh.feature_extraction import EfficientFCParameters, MinimalFCParameters

from tsfresh import extract_features
from multiprocessing import Process
import time
start= time.time()

if __name__ == '__main__':
    download_robot_execution_failures()
    timeseries, y = load_robot_execution_failures()
    timeseries = timeseries[0:100]
    # extracted_features = extract_features(timeseries, column_id="id", column_sort="time")
    extracted_features = extract_features(timeseries, column_id="id", column_sort="time", default_fc_parameters=MinimalFCParameters())

    print(extracted_features)
    print(time.time()-start)