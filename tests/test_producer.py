from flow.producer import DataProducer


p = DataProducer()
for i in range(100):
    p.send_stream(topic="test-data", value=i)