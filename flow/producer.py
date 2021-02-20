import certifi
from confluent_kafka import Producer
import socket
import pickle


class DataProducer(Producer):

    def __init__(self, serializer=pickle.dumps):
        conf = {'bootstrap.servers': "pkc-4r297.europe-west1.gcp.confluent.cloud:9092",
                "security.protocol": "",
                "sasl.mechanisms": "",
                "sasl.username": "54KW7VWPPTJIL74Y",
                "sasl.password": "UpsXcoDKhvgz5v5w47fuFwEpV9WidGUdLLt7YKzT69U/0jS6Pb321qKepzzSAdOF",
                "security.protocol": "SASL_SSL",
                "sasl.mechanisms": "PLAIN",
                "ssl.ca.location": certifi.where(),
                'client.id': socket.gethostname()
        }

        super().__init__(conf)
        self.serializer = serializer

    def send_stream(self, topic=None, key=None, value=None,):
        super().produce(topic=topic, key=self.serializer(key), value=self.serializer(value), callback=self.acked)
        super().poll(1)

    def acked(self, error, message):
        if error is not None:
            print(f"Failed to deliver message: {message} {error}")
        else:
            print(f"Message produced: {message}")




