
import numpy as np
import pickle
from kafka import KafkaProducer
from kafka.errors import KafkaError


A = np.arange(9).reshape((3,3))
print(A)
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer= pickle.dumps)


# Asynchronous by default
future = producer.send('sample', A)
producer.flush()

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    pass

# Successful result returns assigned partition and offset
print(record_metadata.topic)
print(record_metadata.partition)
print(record_metadata.offset)
