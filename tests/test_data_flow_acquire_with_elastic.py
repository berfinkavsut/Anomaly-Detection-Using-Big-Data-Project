import time
from flow.system_flow import SystemFlow
from utils.alert import Alert

props = {'xStream': {}, 'IForest': {}, 'RRCF': {}}

ens_props = {'Ensemble (IForest and RRCF)': {'IForest': {}, 'RRCF': {}},
             'Ensemble (RRCF and xStream)': {'RRCF': {}, 'xStream': {}},
             'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}}
             }

data_dim = 10

param = {
        'autoencoder':
             {'latent_dim': data_dim,
             'batch_size': 1,
             'epoch_no': 5,
             'optimizer': 'adam',
             'loss': 'mse',}
         }
col_names = [ "duration", "source_ip", "destination_ip", "protocol", "packet_len","dif_serv",
            "flag", "ip_vers", "src_port", "dst_port", "data_len", "seq", "seq_raw", "next_seq", "ack", "ack_raw",
            "flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push",
            "flags_reset", "flags_syn", "flags_fin", "win_size", "checksum", "checksum_status",
            "urgent_pointer", "proto_type", "proto_size", "hw_type", "hw_size", "hw_opcode", "src_hw_mac",
            "dst_hw_mac"]
selected_features = {'autoencoder': col_names}

selected_feature_extractors = ['autoencoder']

fe_config = {"selected_feature_extractors": selected_feature_extractors, "selected_features": selected_features, "param": param}

topic = "Device1"
system_flow = SystemFlow(props, ens_props, config="cloud", fe=True, fe_config=fe_config, user="elastic",
                 psw="changeme", elk_index="test_flow", verbose=True, with_elastic=True, with_dataset=False)


system_flow.create_stream(topic)

thresholds= {'0.5': [0.5]}

i = 0

alarm = Alert()
while True:
    if i < 2:
        system_flow.fit_next(topic)
        i += 1
    else:

        s = time.time()
        reduced_data, original_data, probs, ens_probs = system_flow.fit_predict_next(topic)

        #Threshold and alert
        threshold = system_flow.return_threshold()

        probsarray = []
        for key in probs:
            probsarray.append(probs[key][0])

        for key in ens_probs:
            probsarray.append(ens_probs[key][0])

        max_prob = max(probsarray)
        print("maxprob" , max_prob)

        if threshold < max_prob:
            alarm.send_email()

        thresholds = {'threshold': [threshold]}

        # Send to elastic
        system_flow.send_to_elk(original_data, probs, ens_probs, thresholds)


        # # Update hyperparameters
        # hyperparameters = system_flow.return_hyperparameter()
        #
        # if old_hyp != hyperparameters:
        #     system_flow.update(hyperparameters)
        #
        # old_hyp = hyperparameters










