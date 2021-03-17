from flow.consumer import DataConsumer
from transformers import network_data_transformer
import pandas as pd

c = DataConsumer(config="cloud", verbose=False)

streamer = c.stream_data("test-data")
b = network_data_transformer
pd.set_option('display.max_columns', None)
while True:
    for data in streamer:
        print(b.network_data_transformer(data))

