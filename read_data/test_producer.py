from read_data.producer import DataProducer


p = DataProducer()
for i in range(100):
    p.send_stream(topic="Test", value=i)