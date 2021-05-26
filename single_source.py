import time
from flow.system_flow import SystemFlow


def single_process(topic="Test"):

    props = {'xStream': {}, 'IForest': {}, 'Loda': {}}

    ens_props = {'Ensemble (IForest and Loda)': {'IForest': {}, 'Loda': {}},
                 'Ensemble (Loda and xStream)': {'Loda': {}, 'xStream': {}},
                 'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}}
                 }

    data_dim = 10

    param = {
        'autoencoder':
            {'latent_dim': data_dim,
             'batch_size': 1,
             'epoch_no': 5,
             'optimizer': 'adam',
             'loss': 'mse', }
    }

    col_names = ["duration", "source_ip", "destination_ip", "protocol", "packet_len", "dif_serv",
                 "flag", "ip_vers", "src_port", "dst_port", "data_len", "seq", "seq_raw", "next_seq", "ack", "ack_raw",
                 "flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push",
                 "flags_reset", "flags_syn", "flags_fin", "win_size", "checksum", "checksum_status",
                 "urgent_pointer", "proto_type", "proto_size", "hw_type", "hw_size", "hw_opcode", "src_hw_mac",
                 "dst_hw_mac"]

    selected_features = {'autoencoder': col_names}

    selected_feature_extractors = ['autoencoder']

    fe_config = {"selected_feature_extractors": selected_feature_extractors, "selected_features": selected_features, "param": param}


    system_flow = SystemFlow(data_dim, props, ens_props, config="cloud", fe=True, fe_config=fe_config, user="elastic",
                             psw="sBnnldRLdLiJmZotTSbo", verbose=True)

    system_flow.create_stream(topic)

    i = 0
    while True:
        if i < 2:
            system_flow.fit_next(topic)
            i += 1
        else:
            reduced_data, original_data, probs, ens_probs = system_flow.fit_predict_next(topic)
            system_flow.send_to_elk(original_data, probs, ens_probs, topic)


if __name__ == "__main__":
    single_process("device1")

