from flow.consumer import DataConsumer

c = DataConsumer()
streamer = c.stream_data("Test")

while True:
    for data in streamer:
        print(data)

