from flow.consumer import DataConsumer

c = DataConsumer()
streamer = c.stream_data("Test")

for data in streamer:
    print(data)

