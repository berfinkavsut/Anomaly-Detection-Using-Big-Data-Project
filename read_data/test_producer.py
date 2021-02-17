from read_data.producer import DataProducer


p = DataProducer()
value = None #whateva u want string array vs

for i in range(10):
    p.send_stream(topic="Test", value=value)