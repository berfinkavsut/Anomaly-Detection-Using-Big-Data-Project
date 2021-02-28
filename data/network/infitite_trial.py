import live_network_data


if __name__ == "__main__":

    a = live_network_data

    count = 0
    while True:
        df = a.get_live_network_data("Wi-Fi", 10)
        print(str(count) + " -> " + str(df.shape))
        print(df)
        count = count + 1