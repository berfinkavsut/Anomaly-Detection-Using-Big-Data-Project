#Check if cython code has been compiled
import os
import subprocess

use_extrapolation=False #experimental correlation code
if use_extrapolation:
    print("Importing AfterImage Cython Library")
    if not os.path.isfile("AfterImage.c"): #has not yet been compiled, so try to do so...
        cmd = "python setup.py build_ext --inplace"
        subprocess.call(cmd,shell=True)
#Import dependencies
from kitsune_files.netStat import netStat
import csv
import numpy as np
print("Importing Scapy Library")
from scapy.all import *
import os.path
import platform
import subprocess


#Extracts Kitsune features from given pcap file one packet at a time using "get_next_vector()"
# If wireshark is installed (tshark) it is used to parse (it's faster), otherwise, scapy is used (much slower).
# If wireshark is used then a tsv file (parsed version of the pcap) will be made -which you can use as your input next time
class FE:
    def __init__(self,file_path,df,limit=np.inf):
        self.path = file_path
        self.limit = limit
        self.parse_type = None #unknown
        self.curPacketIndx = 0
        self.tsvin = None #used for parsing TSV file
        self.scapyin = None #used for parsing pcap with scapy
        self.df = df

        ### Prep pcap ##
        self.__prep__()

        ### Prep Feature extractor (AfterImage) ###
        maxHost = 100000000000
        maxSess = 100000000000
        self.nstat = netStat(np.nan, maxHost, maxSess)

    def _get_tshark_path(self):
        if platform.system() == 'Windows':
            return 'C:\Program Files\Wireshark\\tshark.exe'
        else:
            system_path = os.environ['PATH']
            for path in system_path.split(os.pathsep):
                filename = os.path.join(path, 'tshark')
                if os.path.isfile(filename):
                    return filename
        return ''

    def __prep__(self):
        ### Find file: ###
        if not os.path.isfile(self.path):  # file does not exist
            print("File: " + self.path + " does not exist")
            #raise Exception()

        ### check file type ###
        type = self.path.split('.')[-1]

        self._tshark = self._get_tshark_path()
        ##If file is TSV (pre-parsed by wireshark script)
        if type == "tsv":
            self.parse_type = "tsv"

        ##If file is pcap
        elif type == "pcap" or type == 'pcapng':
            # Try parsing via tshark dll of wireshark (faster)
            if os.path.isfile(self._tshark):
                self.pcap2tsv_with_tshark()  # creates local tsv file
                self.path += ".tsv"
                self.parse_type = "tsv"
            else: # Otherwise, parse with scapy (slower)
                print("tshark not found. Trying scapy...")
                self.parse_type = "scapy"
        else:
            print("File: " + self.path + " is not a tsv or pcap file")
            raise Exception()

        ### open readers ##
        if self.parse_type == "tsv":
            maxInt = sys.maxsize
            decrement = True
            while decrement:
                # decrease the maxInt value by factor 10
                # as long as the OverflowError occurs.
                decrement = False
                try:
                    csv.field_size_limit(maxInt)
                except OverflowError:
                    maxInt = int(maxInt / 10)
                    decrement = True

            print("counting lines in file...")
            num_lines = sum(1 for line in open(self.path))
            print("There are " + str(num_lines) + " Packets.")
            #self.limit = min(self.limit, num_lines-1)
            #self.tsvinf = open(self.path, 'rt', encoding="utf8")
            # #print('tsvinfintype', self.tsvinf.type())
            #self.tsvin = csv.reader(self.tsvinf, delimiter='\t')
            #print('tsvinintype', self.tsvin.type())

            self.row_iterator = self.df.iterrows()


            #row = self.tsvin.__next__() #move iterator past header


        else: # scapy
            print("Reading PCAP file via Scapy...")
            self.scapyin = rdpcap(self.path)
            #self.limit = len(self.scapyin)
            print("Loaded " + str(len(self.scapyin)) + " Packets.")

    def get_next_vector(self):
        # if self.curPacketIndx == self.limit:
        #     if self.parse_type == 'tsv':
        #         self.tsvinf.close()
        #     return []

        ### Parse next packet ###
        if self.parse_type == "tsv":
            row = self.tsvin.__next__()
            print(row)
            row = list(next(self.row_iterator)[1])
            print('here')
            print(row)

            IPtype = np.nan
            timestamp = row[0].get_default_value() #??
            framelen = row[1].get_default_value() #??
            framelen = 0.1
            #print(framelen.type(), "aaaaaaaaaaaaa")
            srcIP = row[1].get_default_value()
            dstIP = row[2].get_default_value()
            # if row[4] != '':  # IPv4
            #     srcIP = row[4]
            #     dstIP = row[5]
            #     IPtype = 0
            # elif row[17] != '':  # ipv6
            #     srcIP = row[17]
            #     dstIP = row[18]
            #     IPtype = 1

            if row[8] == '4': #ipv4
                #srcIP = row[41].get_default_value()
                #dstIP = row[43].get_default_value()
                IPtype = 0

            if row[8] == '6': #ipv6
                srcIP = row[1].get_default_value()
                dstIP = row[2].get_default_value()
                IPtype = 1

            #TCP UDP
            # srcproto = row[6] + row[8]  # UDP or TCP port: the concatenation of the two port strings will will results in an OR "[tcp|udp]"
            # dstproto = row[7] + row[9]  # UDP or TCP port
            srcproto = row[9].get_default_value()
            dstproto = row[10].get_default_value()
            udp_or_tcp = row[4] == 'tcp' or row[4] == 'udp'
            srcMAC = row[1].get_default_value()
            dstMAC = row[2].get_default_value()
            if row[40]:
                srcMAC = row[40].get_default_value()
                dstMAC = row[42].get_default_value()


            #if srcproto == '':  # it's a L2/L1 level protocol
            if udp_or_tcp is False: # it's a L2/L1 level protocol
                if row[4] == 'arp':  # is ARP
                    srcproto = 'arp'
                    dstproto = 'arp'
                    srcIP = row[41].get_default_value() # src IP (ARP)
                    dstIP = row[43].get_default_value()  # dst IP (ARP)
                    IPtype = 0
                elif row[4] == 'icmp':  # is ICMP
                    srcproto = 'icmp'
                    dstproto = 'icmp'
                    IPtype = 0
                #elif srcIP + srcproto + dstIP + dstproto == '':  # some other protocol
                else:
                    srcIP = row[40].get_default_value()  # src MAC
                    dstIP = row[42].get_default_value()  # dst MAC

        elif self.parse_type == "scapy":
            packet = self.scapyin[self.curPacketIndx]
            IPtype = np.nan
            timestamp = packet.time
            framelen = len(packet)
            if packet.haslayer(IP):  # IPv4
                srcIP = packet[IP].src
                dstIP = packet[IP].dst
                IPtype = 0
            elif packet.haslayer(IPv6):  # ipv6
                srcIP = packet[IPv6].src
                dstIP = packet[IPv6].dst
                IPtype = 1
            else:
                srcIP = ''
                dstIP = ''

            if packet.haslayer(TCP):
                srcproto = str(packet[TCP].sport)
                dstproto = str(packet[TCP].dport)
            elif packet.haslayer(UDP):
                srcproto = str(packet[UDP].sport)
                dstproto = str(packet[UDP].dport)
            else:
                srcproto = ''
                dstproto = ''

            srcMAC = packet.src
            dstMAC = packet.dst
            if srcproto == '':  # it's a L2/L1 level protocol
                if packet.haslayer(ARP):  # is ARP
                    srcproto = 'arp'
                    dstproto = 'arp'
                    srcIP = packet[ARP].psrc  # src IP (ARP)
                    dstIP = packet[ARP].pdst  # dst IP (ARP)
                    IPtype = 0
                elif packet.haslayer(ICMP):  # is ICMP
                    srcproto = 'icmp'
                    dstproto = 'icmp'
                    IPtype = 0
                elif srcIP + srcproto + dstIP + dstproto == '':  # some other protocol
                    srcIP = packet.src  # src MAC
                    dstIP = packet.dst  # dst MAC
        else:
            return []

        self.curPacketIndx = self.curPacketIndx + 1


        ### Extract Features
        try:
            return self.nstat.updateGetStats(IPtype, srcMAC, dstMAC, srcIP, srcproto, dstIP, dstproto,
                                                 int(framelen),
                                                 float(timestamp))
        except Exception as e:
            print(e)
            return []


    def pcap2tsv_with_tshark(self):
        print('Parsing with tshark...')
        fields = "-e frame.time_epoch -e frame.len -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e icmp.type -e icmp.code -e arp.opcode -e arp.src.hw_mac -e arp.src.proto_ipv4 -e arp.dst.hw_mac -e arp.dst.proto_ipv4 -e ipv6.src -e ipv6.dst"
        cmd =  '"' + self._tshark + '" -r '+ self.path +' -T fields '+ fields +' -E header=y -E occurrence=f > '+self.path+".tsv"
        subprocess.call(cmd,shell=True)
        print("tshark parsing complete. File saved as: "+self.path +".tsv")

    def get_num_features(self):
        return len(self.nstat.getNetStatHeaders())
