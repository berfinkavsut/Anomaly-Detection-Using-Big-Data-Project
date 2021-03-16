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
            conf = {'bootstrap.servers': "pkc-4r297.europe-west1.gcp.confluent.cloud:9092",
                    "security.protocol": "",
                    "sasl.mechanisms": "",
                    "sasl.username": "54KW7VWPPTJIL74Y",
                    "sasl.password": "UpsXcoDKhvgz5v5w47fuFwEpV9WidGUdLLt7YKzT69U/0jS6Pb321qKepzzSAdOF",
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




