from flow.producer import DataProducer


p = DataProducer(config="cloud")

for i in range(10):
    p.send_stream(topic="device1", value=i)