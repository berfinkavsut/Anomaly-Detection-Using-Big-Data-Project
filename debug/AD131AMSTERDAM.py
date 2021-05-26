import pickle
from pathlib import Path
from flow import Train
from pysad.evaluation import AUROCMetric, PrecisionMetric
import pandas as pd

from custom_modules.feature_extractor import FeatureExtractor



class DEBUG:

    def __init__(self, props=None, ens_props=None, fe=False, fe_config=None):

        self.train = Train(model_properties=props, ensemble_model_properties=ens_props)

        self.fe = fe

        if self.fe:
            self.extractor = FeatureExtractor(**fe_config)

        self.auroc_probs = dict.fromkeys(props.keys())
        self.auroc_ens = dict.fromkeys(ens_props.keys())


        for key in self.auroc_probs.keys():
            self.auroc_probs[key] = AUROCMetric()


        for key in self.auroc_ens.keys():
            self.auroc_ens[key] = AUROCMetric()


        self.i = 0


    def fit_next(self, X):
        self.train.fit(X)
        return X


    def predict_next(self, X):
        prediction = self.train.predict(X)
        return prediction


    def fit_predict_next(self, X):

        if self.fe:
            X = self.extractor.fit_transform(
                pd.DataFrame(data=X, columns=[ "duration", "source_ip", "destination_ip", "protocol", "packet_len","dif_serv",
            "flag", "ip_vers", "src_port", "dst_port", "data_len", "seq", "seq_raw", "next_seq", "ack", "ack_raw",
            "flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push",
            "flags_reset", "flags_syn", "flags_fin", "win_size", "checksum", "checksum_status",
            "urgent_pointer", "proto_type", "proto_size", "hw_type", "hw_size", "hw_opcode", "src_hw_mac",
            "dst_hw_mac"])
            )["autoencoder"].to_numpy()


        self.train.fit(X)
        return self.train.predict(X)


    def updateAUROC(self, Y, pred):
        probs, ens = pred

        for key, value in probs.items():
            v = (value[0])
            self.auroc_probs[key].update(Y, v)

        for key, value in ens.items():
            self.auroc_ens[key].update(Y, v)


    def getAUROC(self):
        print("------AUROC-----")
        for key, value in self.auroc_probs.items():
            print(f"{key}: {value.get()}")


        for key, value in self.auroc_ens.items():
            print(f"{key}: {value.get()}")



    def save_trained_models(self, path="saved_models"):
        models, ensemble_models = self.train.get_models()

        if models is not None:
            Path(f"{path}/models").mkdir(parents=True, exist_ok=True)
            for key in models.keys():
                with open(f"{path}/models/{key}", 'wb') as file:
                    pickle.dump(models[key], file)

        if ensemble_models is not None:
            Path(f"{path}/ensemble_models").mkdir(parents=True, exist_ok=True)
            for key in ensemble_models.keys():
                with open(f"{path}/ensemble_models/{key}", 'wb') as file:
                    pickle.dump(ensemble_models[key], file)
