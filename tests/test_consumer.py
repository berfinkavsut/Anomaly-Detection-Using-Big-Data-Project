from flow.consumer import DataConsumer

c = DataConsumer(config="cloud", topic="device1")

while True:
    print(next(c))


