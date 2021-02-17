from read_data.consumer import DataConsumer
import time

c = DataConsumer()
streamer = c.stream_data("Test")

for data in streamer:
    print(data)

