import time
from flow.system_flow import SystemFlow
from utils.animate_live import AnimateLive
import numpy as np

props = {'xStream': {}, 'IForest': {}, 'Loda': {}}

ens_props = {'Ensemble (IForest and Loda)': {'IForest': {}, 'Loda': {}},
             'Ensemble (Loda and xStream)': {'Loda': {}, 'xStream': {}},
             'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}},}

#param is dictionary of dictionaries
param = {'autoencoder': {'latent_dim': 10,
                         'batch_size': 1,
                         'epoch_no': 5,
                         'optimizer': 'adam',
                         'loss': 'mse',
                         }
         }

selected_features = {'autoencoder': ["a", "b", "d", "a2", "b2", "d2", "a3", "b3", "d3"]
                     }

selected_feature_extractors = ['autoencoder']

fe_config = {"selected_feature_extractors": selected_feature_extractors, "selected_features": selected_features, "param": param}
system_flow = SystemFlow(122, props, ens_props, config="cloud", fe=True, fe_config=fe_config, verbose=True)
topic = "test-AD"
system_flow.create_stream(topic)
anim = AnimateLive(ax_num=6, x_labels=["Time"] * 6, y_labels=["xStream", "IForest", "Loda", "Ensemble (IForest and Loda)",
                                                    "Ensemble (Loda and xStream)", "Ensemble (xStream and IForest)"])
i = 0
train_iter = 20
while True:

    if i < train_iter:
        system_flow.fit_next(topic)
        i += 1
    else:
        s = time.time()
        probs, ens_probs, data = system_flow.fit_predict_next(topic)
        print(probs, ens_probs, data)

        update_arr = np.array([])

        for key in probs.keys():
            update_arr = np.append(update_arr, probs[key])

        for key in ens_probs.keys():
            update_arr = np.append(update_arr, ens_probs[key])

        anim.update_data(update_arr, time.time()-s)
        anim.update_graph()
