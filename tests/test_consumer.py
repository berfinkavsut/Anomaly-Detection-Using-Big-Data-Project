from flow.consumer import DataConsumer

c = DataConsumer(config="cloud")
streamer = c.stream_data("test-data")

for data in streamer:
    print(data)

