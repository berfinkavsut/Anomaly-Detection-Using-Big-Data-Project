import certifi
from confluent_kafka import Producer
import socket
import pickle


class DataProducer(Producer):

    def __init__(self, serializer=pickle.dumps, config="local", verbose=True):

        if config is "local":
            conf = {'bootstrap.servers': "localhost:9092",
               'client.id': socket.gethostname()}

        elif config is "cloud":
            conf = {'bootstrap.servers': "pkc-lzvrd.us-west4.gcp.confluent.cloud:9092",
                    "security.protocol": "",
                    "sasl.mechanisms": "",
                    "sasl.username": "PAMBITHEWTHX3PP4",
                    "sasl.password": "G8QVRHA85d9yZRt7z2olWWij8MSfVhTxAbxr/pu43YJL6WXQwe0ml5q8JyaVj2w9",
                    "security.protocol": "SASL_SSL",
                    "sasl.mechanisms": "PLAIN",
                    "ssl.ca.location": certifi.where(),
                    'client.id': socket.gethostname()}
        else:
            raise Exception("The config option has to be cloud or local")

        super().__init__(conf)
        self.serializer = serializer
        self.verbose = verbose

    def send_stream(self, topic=None, key=None, value=None,):
        callback = None
        if self.verbose:
            callback = self.acked
        super().produce(topic=topic, key=self.serializer(key), value=self.serializer(value), callback=callback)
        super().poll(1)

    def acked(self, error, message):
        if error is not None:
            print(f"Failed to deliver message: {message} {error}")
        else:
            print(f"Message produced: {message}")




