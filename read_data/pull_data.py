from kafka import KafkaConsumer

class pullData:

    def __init__(self, topic=None, group_id=None, servers=None):
        self.consumer = KafkaConsumer(topic, group_id=group_id, bootstrap_servers=servers)


