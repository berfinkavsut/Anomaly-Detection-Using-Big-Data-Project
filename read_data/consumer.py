import certifi
from confluent_kafka import Consumer, KafkaError
import pickle

class DataConsumer(Consumer):

    def __init__(self, deserializer=pickle.loads):

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

        super().__init__(conf)
        self.deserializer = deserializer

    def stream_data(self, topic=None):

        super().subscribe([topic])

        try:

            while True:

                msg = super().poll(0.1)

                if msg is None:

                    continue

                elif not msg.error():

                    value = self.deserializer(msg.value())

                    print('Received message: {0}'.format(value))

                    yield value

                elif msg.error().code() == KafkaError._PARTITION_EOF:

                    print('End of partition reached {0}/{1}'
                          .format(msg.topic(), msg.partition()))
                else:

                    print('Error occured: {0}'.format(msg.error().str()))


        except KeyboardInterrupt:
            pass

        finally:
            super().close()


    #
    #
    # def create_batch(self, topic=None, batch_size=64):
