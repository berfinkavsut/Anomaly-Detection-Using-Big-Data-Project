from flow.consumer import DataConsumer

c = DataConsumer()
streamer = c.stream_data("saa")

for data in streamer:
    print(data)

