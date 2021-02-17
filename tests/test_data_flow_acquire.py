from read_data.consumer import DataConsumer
import time
from train import Train
import numpy as np

#
exec(open('test_data_flow_send.py').read())

# , 'xStream': {}, 'IForest': {}, 'Loda': {'contamination': 0.2}
props = {'xStream': {}}
# ens_props = {'Ensemble (Loda with Contamination: 0.3, IForest)': {'Loda': {'contamination': 0.3}, 'IForest': {}},
#              'Ensemble (Loda with Contamination: 0.1, IForest)': {'Loda': {'contamination': 0.1}, 'IForest': {}}}

train = Train(num_features=9, model_properties=props, ensemble_model_properties=None)



c = DataConsumer()
streamer = c.stream_data("Test")


i = 1
for data in streamer:
    if i < 10:

        train.fit(data[0])

    else:
        j = 1
        s = time.time()
        train.predict(data[0])
        e = time.time()
        print(f"Train in seconds: {(e - s)/j}")
        j += 1
    i += 1
    # probs = train.predict(data[0])[0]
