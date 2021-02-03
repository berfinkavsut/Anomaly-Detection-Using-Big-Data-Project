from kafka import KafkaConsumer
import pickle
import numpy as np


consumer = KafkaConsumer('sample', group_id=None, auto_offset_reset='earliest', value_deserializer = pickle.loads)
while True:
    msg = next(consumer)
    print(msg.value)
