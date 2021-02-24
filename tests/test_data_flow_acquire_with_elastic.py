import time
from flow.system_flow import SystemFlow
from utils.animate_live import AnimateLive
import numpy as np
from elasticsearch import Elasticsearch
import pandas as pd

props = {'xStream': {}, 'IForest': {}, 'Loda': {}}

ens_props = {'Ensemble (IForest and Loda)': {'IForest': {}, 'Loda': {}},
             'Ensemble (Loda and xStream)': {'Loda': {}, 'xStream': {}},
             'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}},}

system_flow = SystemFlow(9, props, ens_props)
topic = "Test"
system_flow.create_stream(topic)
anim = AnimateLive(ax_num=6, x_labels=["Time"] * 6, y_labels=["xStream", "IForest", "Loda", "Ensemble (IForest and Loda)",
                                                    "Ensemble (Loda and xStream)", "Ensemble (xStream and IForest)"])

for i in range(1000):

    if i < 3:
        system_flow.fit_next(topic)
    else:
        s = time.time()
        probs, ens_probs, data = system_flow.fit_predict_next(topic)
        print(probs, ens_probs, data)

        update_arr = np.array([])

        for key in probs.keys():
            update_arr = np.append(update_arr, probs[key])

        for key in ens_probs.keys():
            update_arr = np.append(update_arr, ens_probs[key])

        anim.update_data(update_arr, time.time()-s)
        anim.update_graph()


import logging
from logging import StreamHandler
import logstash
import sys

host = 'localhost'

test_logger = logging.getLogger('python-logstash-logger')
test_logger.setLevel(logging.INFO)
test_logger.addHandler(logstash.TCPLogstashHandler(host, 5044, version=1))
test_logger.addHandler(StreamHandler())

try:
    test_logger.error('python-logstash: test logstash error message.')
    test_logger.info('python-logstash: test logstash info message.')
    test_logger.warning('python-logstash: test logstash warning message.')

    # add extra field to logstash message
    extra = {
        'test_string': 'python version: ' + repr(sys.version_info),
        'test_boolean': True,
        'test_dict': {'a': 1, 'b': 'c'},
        'test_float': 1.23,
        'test_integer': 123,
        'test_list': [1, 2, '3'],
    }
    test_logger.info('python-logstash: test extra fields', extra=extra)
except:
    print("Error")
