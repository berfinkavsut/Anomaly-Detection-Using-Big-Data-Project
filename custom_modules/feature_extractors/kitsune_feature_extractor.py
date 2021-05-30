import numpy as np
import pandas as pd

# Prep AfterImage cython package
import os
import subprocess
import pyximport; pyximport.install()
import custom_modules.feature_extractors.kitsune_after_image as af
# import AfterImage_NDSS as af

from custom_modules.feature_extractors.base_feature_extractor import BaseFeatureExtractor


use_extrapolation = False  # experimental correlation code
if use_extrapolation:
    print("Importing AfterImage Cython Library")
    if not os.path.isfile("AfterImage.c"):  # has not yet been compiled, so try to do so...
        cmd = "python setup.py build_ext --inplace"
        subprocess.call(cmd, shell=True)


class KitsuneFeatureExtractor(BaseFeatureExtractor):

    feature_extractor_name = 'kitsune_feature_extractor'

    def __init__(self, param, selected_features):
        """
        :param param: dictionary for model parameters
        :param selected_features: selected features to extract features
        """

        super().__init__(param=param, selected_features=selected_features)

        # limit = np.inf
        # Lambdas = np.nan
        # HostLimit = 100000000000
        # HostSimplexLimit = 100000000000


        # Lambdas
        if np.isnan(param['Lambdas']):
            self.Lambdas = [5, 3, 1, .1, .01]
        else:
            self.Lambdas = param['Lambdas']

        # HT Limits
        self.limit = param['limit']
        self.HostLimit = param['HostLimit']
        self.HostSimplexLimit = param['HostSimplexLimit']
        self.SessionLimit = self.HostSimplexLimit * self.HostLimit * self.HostLimit  # *2 since each dual creates 2 entries in memory
        self.MAC_HostLimit = self.HostLimit * 10

        # HTs
        # self.HT_jit = []
        # self.HT_MI = []
        # self.HT_H = []
        # self.HT_Hp = []

        # Prep Feature extractor (AfterImage) #
        # HTs
        self.HT_jit = af.incStatDB(limit=self.HostLimit * self.HostLimit)  # H-H Jitter Stats
        self.HT_MI = af.incStatDB(limit=self.MAC_HostLimit)  # MAC-IP relationships
        self.HT_H = af.incStatDB(limit=self.HostLimit)  # Source Host BW Stats
        self.HT_Hp = af.incStatDB(limit=self.SessionLimit)  # Source Host BW Stats

        self.curPacketIndx = 0

    def fit(self, X=None):
        pass

    def transform(self, X):
        pkt = X
        features_extracted = self.get_next_vector(pkt)
        return features_extracted

    def fit_transform(self, X):
        self.fit(X)
        features_extracted = self.transform(X)
        return features_extracted

    def get_next_vector(self, pkt):
        if pkt is None:
            return []
        else:

            IPtype = np.nan
            timestamp = 0
            framelen = 0
            srcIP = ''
            dstIP = ''
            srcproto = ''
            dstproto = ''
            srcMAC = ''
            dstMAC = ''
            protocol_name = ''

            if pkt['ip_vers'] == 4:
                IPtype = 0
            elif pkt['ip_vers'] == 6:
                IPtype = 1

            if pkt['time'] is not np.nan:
                timestamp = float(pkt['time'])

            if pkt['packet_len'] is not np.nan:
                framelen = int(pkt['packet_len'])

            if pkt['source_ip'] is not np.nan:
                srcIP = str(pkt['source_ip'])

            if pkt['destination_ip'] is not np.nan:
                dstIP = str(pkt['destination_ip'])

            if pkt['src_port'] is not np.nan:
                srcproto = str(pkt['src_port'])

            if pkt['dst_port'] is not np.nan:
                dstproto = str(pkt['dst_port'])

            if pkt['src_hw_mac'] is not np.nan:
                srcMAC = str(pkt['src_hw_mac'])

            if pkt['dst_hw_mac'] is not np.nan:
                dstMAC = str(pkt['dst_hw_mac'])

            if pkt['protocol_name'] is not np.nan:
                protocol_name = str(pkt['protocol_name'])

            if protocol_name == 'arp':  # it's a L2/L1 level protocol
                srcproto = 'arp'
                dstproto = 'arp'
                IPtype = 0
            elif protocol_name != ('tcp' or 'udp'):
                srcproto = 'other'
                dstproto = 'other'
                IPtype = 0

            if srcIP == '':
                srcIP = srcMAC  # src MAC
            if dstIP == '':  # some other protocol (not tcp/udp/arp)
                dstIP = dstMAC  # dst MAC

            """
            print('IPtype:', IPtype, ' type:', type(IPtype))
            print('srcMAC:', srcMAC, ' type:', type(srcMAC))
            print('dstMAC:', dstMAC, ' type:', type(dstMAC))
            print('srcIP:', srcIP, ' type:', type(srcIP))
            print('srcproto:', srcproto, ' type:', type(srcproto))
            print('dstIP:', dstIP, ' type:', type(dstIP))
            print('dstproto:', dstproto, ' type:', type(dstproto))
            print('framelen:', framelen, ' type:', type(framelen))
            print('timestamp:', timestamp, ' type:', type(timestamp))
            print('PROTOCOL:', protocol_name)
            """

            self.curPacketIndx = self.curPacketIndx + 1

        # Extract Features #
        try:
            return self.updateGetStats(IPtype, srcMAC, dstMAC, srcIP, srcproto, dstIP, dstproto, framelen, timestamp)
        except Exception as e:
            print(e)
            return []

    def get_num_features(self):
        return len(self.getNetStatHeaders())

    def findDirection(self, IPtype, srcIP, dstIP, eth_src, eth_dst):
        # cpp: this is all given to you in the direction string of the instance
        # (NO NEED FOR THIS FUNCTION)

        if IPtype == 0:  # is IPv4
            lstP = srcIP.rfind('.')
            src_subnet = srcIP[0:lstP:]
            lstP = dstIP.rfind('.')
            dst_subnet = dstIP[0:lstP:]
        elif IPtype == 1:  # is IPv6
            src_subnet = srcIP[0:round(len(srcIP)/2):]
            dst_subnet = dstIP[0:round(len(dstIP)/2):]
        else:  # no Network layer, use MACs
            src_subnet = eth_src
            dst_subnet = eth_dst

        return src_subnet, dst_subnet

    def updateGetStats(self, IPtype, srcMAC, dstMAC, srcIP, srcProtocol, dstIP, dstProtocol, datagramSize, timestamp):
        # Host BW: Stats on the srcIP's general Sender Statistics
        # Hstat = np.zeros((3*len(self.Lambdas,)))
        # for i in range(len(self.Lambdas)):
        #     Hstat[(i*3):((i+1)*3)] = self.HT_H.update_get_1D_Stats(srcIP, timestamp, datagramSize, self.Lambdas[i])

        # MAC.IP: Stats on src MAC-IP relationships
        MIstat = np.zeros((3*len(self.Lambdas,)))
        for i in range(len(self.Lambdas)):
            MIstat[(i*3):((i+1)*3)] = self.HT_MI.update_get_1D_Stats(srcMAC+srcIP, timestamp, datagramSize, self.Lambdas[i])

        # Host-Host BW: Stats on the dual traffic behavior between srcIP and dstIP
        HHstat = np.zeros((7*len(self.Lambdas,)))
        for i in range(len(self.Lambdas)):
            HHstat[(i*7):((i+1)*7)] = self.HT_H.update_get_1D2D_Stats(srcIP, dstIP,timestamp,datagramSize,self.Lambdas[i])

        # Host-Host Jitter:
        HHstat_jit = np.zeros((3*len(self.Lambdas,)))
        for i in range(len(self.Lambdas)):
            HHstat_jit[(i*3):((i+1)*3)] = self.HT_jit.update_get_1D_Stats(srcIP+dstIP, timestamp, 0, self.Lambdas[i],isTypeDiff=True)

        # Host-Host BW: Stats on the dual traffic behavior between srcIP and dstIP
        HpHpstat = np.zeros((7*len(self.Lambdas,)))

        if srcProtocol == 'arp':
            for i in range(len(self.Lambdas)):
                HpHpstat[(i*7):((i+1)*7)] = self.HT_Hp.update_get_1D2D_Stats(srcMAC, dstMAC, timestamp, datagramSize, self.Lambdas[i])
        else:  # some other protocol (e.g. TCP/UDP)
            for i in range(len(self.Lambdas)):
                HpHpstat[(i*7):((i+1)*7)] = self.HT_Hp.update_get_1D2D_Stats(srcIP + srcProtocol, dstIP + dstProtocol, timestamp, datagramSize, self.Lambdas[i])

        return np.concatenate((MIstat, HHstat, HHstat_jit, HpHpstat))  # concatenation of stats into one stat vector

    def getNetStatHeaders(self):
        MIstat_headers = []
        Hstat_headers = []
        HHstat_headers = []
        HHjitstat_headers = []
        HpHpstat_headers = []

        for i in range(len(self.Lambdas)):
            MIstat_headers += ["MI_dir_"+h for h in self.HT_MI.getHeaders_1D(Lambda=self.Lambdas[i],ID=None)]
            HHstat_headers += ["HH_"+h for h in self.HT_H.getHeaders_1D2D(Lambda=self.Lambdas[i],IDs=None,ver=2)]
            HHjitstat_headers += ["HH_jit_"+h for h in self.HT_jit.getHeaders_1D(Lambda=self.Lambdas[i],ID=None)]
            HpHpstat_headers += ["HpHp_" + h for h in self.HT_Hp.getHeaders_1D2D(Lambda=self.Lambdas[i], IDs=None, ver=2)]
        return MIstat_headers + Hstat_headers + HHstat_headers + HHjitstat_headers + HpHpstat_headers


os.chdir('..')
os.chdir('..')

main_dir = os.getcwd()
data_dir = os.path.join(main_dir, "data")
path = os.path.join(data_dir, "Kitsune_45000_not_transformer.csv")

data = pd.read_csv(path)
columns = data.columns
data = pd.DataFrame.to_numpy(data)
data = np.nan_to_num(data)
data = pd.DataFrame(data)
data.columns = columns

# packet_limit = np.Inf  # the number of packets to process
packet_limit = len(data)

param = {'limit': packet_limit,
         'Lambdas': np.nan,
         'HostLimit': 100000000000,
         'HostSimplexLimit': 100000000000}

# param = {'limit': np.inf,
#          'Lambdas': np.nan,
#          'HostLimit': 100000000000,
#          'HostSimplexLimit': 100000000000}

selected_features = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes',
                     'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
                     'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
                     'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
                     'num_access_files', 'num_outbound_cmds', 'is_host_login',
                     ]

kitsune_fe = KitsuneFeatureExtractor(param=param, selected_features=selected_features)
kitsune_fe.fit()

for i in range(10):
    pkt = data.iloc[i]
    # print(pkt)
    features_extracted = kitsune_fe.transform(pkt)
    print(features_extracted)
