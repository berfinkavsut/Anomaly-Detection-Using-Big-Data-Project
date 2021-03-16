from flow.producer import DataProducer


p = DataProducer(config="cloud")

for i in range(100):
    p.send_stream(topic="test-data", value=i)