from flow.consumer import DataConsumer
from transformers import network_data_transformer
c = DataConsumer()
streamer = c.stream_data("Test")
b = network_data_transformer
while True:
    for data in streamer:
        print(b.network_data_transformer(data))

