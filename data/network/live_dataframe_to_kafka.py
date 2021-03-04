"""
Implementation of the request and communication handler.
"""
import concurrent
import os
import time

import numpy as np
import pandas as pd
import pyshark
from flow.producer import DataProducer



# @param interface: the interface
# @param timeout: time interval
if __name__ == "__main__":
    start = time.time()
    cap = pyshark.LiveCapture("Wi-Fi")
    p = DataProducer()

    col_names = [
        "duration", "source", "destination", "protocol", "protocol_name", "bytes", "service", "flag", "ip_vers",
        "src_port", "dst_port", "proto_len", "seq", "seq_raw", "next_seq", "ack", "ack_raw",
        "tcp_flags", "flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push",
        "flags_reset", "flags_syn", "flags_fin", "flags_str", "win", "win_size", "checksum", "checksum_status",
        "urgent_pointer", "stream", "proto_type", "proto_size", "hw_type", "hw_size", "hw_opcode", "src_hw_mac",
        "src_proto_ipv4", "dst_hw_mac", "dst_proto_ipv4"
                ]
    
    df = pd.DataFrame(columns=col_names)
    i = 0
    for packet in cap.sniff_continuously():
        # print("df    --- %s seconds ---" % (time.time() - start))
        # check if TCP layer exist in the i'th packet
        if "TCP" in packet:
            time_relative = i + float(packet.tcp.time_relative)
            srcport = packet.tcp.srcport
            dstport = packet.tcp.dstport
            proto_len = packet.tcp.len
            tcp_seq = packet.tcp.seq
            tcp_seq_raw = packet.tcp.seq_raw
            tcp_nxtseq = packet.tcp.nxtseq
            tcp_ack = packet.tcp.ack
            tcp_ack_raw = packet.tcp.ack_raw
            tcp_flags = packet.tcp.flags
            tcp_flags_res = packet.tcp.flags_res
            tcp_flags_ns = packet.tcp.flags_ns
            tcp_flags_cwr = packet.tcp.flags_cwr
            tcp_flags_ecn = packet.tcp.flags_ecn 
            tcp_flags_urg = packet.tcp.flags_urg
            tcp_flags_ack = packet.tcp.flags_ack
            tcp_flags_push = packet.tcp.flags_push
            tcp_flags_reset = packet.tcp.flags_reset
            tcp_flags_syn = packet.tcp.flags_syn
            tcp_flags_fin = packet.tcp.flags_fin
            tcp_flags_str = packet.tcp.flags_str
            window_size_value = packet.tcp.window_size_value
            window_size = packet.tcp.window_size
            checksum = packet.tcp.checksum
            checksum_status = packet.tcp.checksum_status
            urgent_pointer = packet.tcp.urgent_pointer
            stream = packet.tcp.stream
            proto_name = packet.tcp.layer_name

        # check if UDP layer exist in the i'th packet        
        elif "UDP" in packet:
            time_relative = packet.udp.time_relative
            srcport = packet.udp.srcport
            dstport = packet.udp.dstport
            proto_len = packet.udp.length
            stream = packet.udp.stream
            proto_name = packet.udp.layer_name
            checksum = packet.udp.checksum
            checksum_status = packet.udp.checksum_status
            tcp_seq = tcp_seq_raw = tcp_nxtseq = tcp_ack = tcp_ack_raw = tcp_flags = tcp_flags_res = tcp_flags_ns = tcp_flags_cwr = tcp_flags_ecn = tcp_flags_urg = tcp_flags_ack = tcp_flags_push = tcp_flags_reset = tcp_flags_syn = tcp_flags_fin = tcp_flags_str = window_size_value = window_size = urgent_pointer = None

        # check if both TCP and UDP layers do not exist in the i'th packet assign None to related objects
        else:   
            time_relative = srcport = dstport = proto_len = tcp_seq = tcp_seq_raw = tcp_nxtseq = tcp_ack = tcp_ack_raw = tcp_flags = tcp_flags_res = tcp_flags_ns = tcp_flags_cwr = tcp_flags_ecn = tcp_flags_urg = tcp_flags_ack = tcp_flags_push = tcp_flags_reset = tcp_flags_syn = tcp_flags_fin = tcp_flags_str = window_size_value = window_size = checksum = checksum_status = urgent_pointer = proto_name = stream = None
          

        # check if IP (ipv4) layer exist in the i'th packet
        if  "IP" in packet:
            ip_src = packet.ip.src
            ip_dst = packet.ip.dst
            ip_proto  = packet.ip.proto 
            ip_dsfield = packet.ip.dsfield
            ip_flags = packet.ip.flags
            ip_version = packet.ip.version

        # check if IPV6 layer exist in the i'th packet        
        elif "IPV6" in packet:  
            ip_src = packet.ipv6.src
            ip_dst = packet.ipv6.dst
            ip_version = packet.ipv6.version
            ip_proto = ip_dsfield = ip_flags = None

        # check if both IP (ipv4) and IPV6 layers do not exist in the i'th packet assign None to related objects
        else:
             ip_src = ip_dst = ip_proto =  ip_dsfield = ip_flags =  ip_version = None    
    
        # check if ARP layer exist in the i'th packet        
        if "ARP" in packet:
            proto_type = packet.arp.proto_type
            proto_size = packet.arp.proto_size
            hw_type = packet.arp.hw_type
            hw_size = packet.arp.hw_size
            hw_opcode = packet.arp.opcode
            src_hw_mac = packet.arp.src_hw_mac
            src_proto_ipv4 = packet.arp.src_proto_ipv4
            dst_hw_mac = packet.arp.dst_hw_mac
            dst_proto_ipv4 =  packet.arp.dst_proto_ipv4
        else:
            proto_type = proto_size = hw_type = hw_size =hw_opcode = src_hw_mac = src_proto_ipv4 = dst_hw_mac = dst_proto_ipv4 = None

        # adding the i'th packets information to the i'th row at the dataframe
        df.loc[0] = [
            time_relative , ip_src , ip_dst , ip_proto, proto_name 
            , packet.length , ip_dsfield , ip_flags , ip_version ,  srcport , dstport 
            , proto_len, tcp_seq , tcp_seq_raw, tcp_nxtseq ,tcp_ack, tcp_ack_raw , tcp_flags , tcp_flags_res
            , tcp_flags_ns ,  tcp_flags_cwr  ,  tcp_flags_ecn , tcp_flags_urg  , tcp_flags_ack , tcp_flags_push , tcp_flags_reset 
            , tcp_flags_syn  ,  tcp_flags_fin  ,  tcp_flags_str  , window_size_value , window_size
            , checksum , checksum_status , urgent_pointer , stream ,  proto_type , proto_size , hw_type , hw_size ,hw_opcode 
            , src_hw_mac , src_proto_ipv4 , dst_hw_mac , dst_proto_ipv4
                    ]
        p.send_stream(topic="Test", value=df)
        print(df)
        print(time.gmtime())
        i = time_relative