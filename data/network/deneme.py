from flow.producer import DataProducer
import live_network_data


if __name__ == "__main__":

    p = DataProducer()
    a = live_network_data
    count = 0
    while True:
        df = a.get_live_network_data("Wi-Fi", 10)
        print(str(count) + " -> " + str(df.shape))
        count = count + 1
        p.send_stream(topic="Test", value= df)