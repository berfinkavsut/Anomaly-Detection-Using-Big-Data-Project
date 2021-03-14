import live_network_data
import pandas as pd
from transformers import network_data_transformer

if __name__ == "__main__":

    a = live_network_data
    b = network_data_transformer

    count = 0
    while True:
        df = a.get_live_network_data("Wi-Fi", 1)
        # print(str(count) + " -> " + str(df.shape))
        pd.set_option('display.max_columns', None)
        # print(df)

        # df.to_excel(r'C:\Users\sevki\Desktop\test4.xlsx',  sheet_name='Your sheet name',  index = False)
        print(b.network_data_transformer(df))
        df.to_excel(r'C:\Users\sevki\Desktop\test4.1.xlsx',  sheet_name='Your sheet name',  index = False)

        count = count + 1
        break