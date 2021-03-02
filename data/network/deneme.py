from flow.producer import DataProducer
if __name__ == "__main__":
    producer = DataProducer()
    for _ in range(10):
        producer.send_stream(value="a")
