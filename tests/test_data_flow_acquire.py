import time
from flow.system_flow import SystemFlow
from utils.animate_live import AnimateLive
import numpy as np

props = {'xStream': {}, 'IForest': {}, 'Loda': {}}

ens_props = {'Ensemble (IForest and Loda)': {'IForest': {}, 'Loda': {}},
             'Ensemble (Loda and xStream)': {'Loda': {}, 'xStream': {}},
             'Ensemble (xStream and IForest)': {'xStream': {}, 'IForest': {}},}

system_flow = SystemFlow(9, props, ens_props)
topic = "Test"
system_flow.create_stream(topic)
anim = AnimateLive(ax_num=6, x_labels=["Time"] * 6, y_labels=["xStream", "IForest", "Loda", "Ensemble (IForest and Loda)",
                                                    "Ensemble (Loda and xStream)", "Ensemble (xStream and IForest)"])

for i in range(1000):

    if i < 3:
        system_flow.fit_next(topic)
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
