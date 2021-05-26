import socket
import certifi
from confluent_kafka import Consumer, KafkaError
import pickle

class DataConsumer(Consumer):

    def __init__(self, topic=None, deserializer=pickle.loads, config="local", verbose=True):

        if config is "local":
            conf = {'bootstrap.servers': 'localhost:9092',
                    'group.id': 'mygroup',
                    'enable.auto.commit': True,
                    'default.topic.config': {'auto.offset.reset': 'smallest'}}

        elif config is "cloud":

            conf = {
                'bootstrap.servers': 'pkc-4r297.europe-west1.gcp.confluent.cloud:9092',
                "security.protocol": "",
                "sasl.mechanisms": "",
                "sasl.username": "54KW7VWPPTJIL74Y",
                "sasl.password": "UpsXcoDKhvgz5v5w47fuFwEpV9WidGUdLLt7YKzT69U/0jS6Pb321qKepzzSAdOF",
                "security.protocol": "SASL_SSL",
                "sasl.mechanisms": "PLAIN",
                "ssl.ca.location": certifi.where(),
                'group.id': 'mygroup',
                'client.id': 'client-1',
                'enable.auto.commit': True,
                'session.timeout.ms': 6000,
                'default.topic.config': {'auto.offset.reset': 'smallest'}
            }
        else:
            raise Exception("The config option has to be cloud or local")


        super().__init__(conf)
        self.deserializer = deserializer
        self.verbose = verbose
        self.topic = topic
        self.rand = "Hello"

        super().subscribe([topic])


    def __iter__(self):
        return self


    def __next__(self):

        try:

            while True:

                msg = super().poll(0.1)

                if msg is None:
                    continue

                elif not msg.error():

                    value = self.deserializer(msg.value())
                    if self.verbose:
                        print(f'Received message: {value}')

                    return value

                elif msg.error().code() == KafkaError._PARTITION_EOF:

                    print('End of partition reached {0}/{1}'
                          .format(msg.topic(), msg.partition()))
                else:

                    print('Error occured: {0}'.format(msg.error().str()))


        except KeyboardInterrupt:
            super().close()
            raise StopIteration()









