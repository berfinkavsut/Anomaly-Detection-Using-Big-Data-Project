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
    cap = pyshark.LiveCapture("Wi-Fi")
    p = DataProducer(config="cloud")
    start = time.time()

    col_names = [
        "date&time", "time", "duration", "source_ip", "destination_ip", "protocol", "protocol_name", "packet_len", "dif_serv",
        "flag", "ip_vers", "src_port", "dst_port", "data_len", "seq", "seq_raw", "next_seq", "ack", "ack_raw",
        "tcp_flags", "flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push",
        "flags_reset", "flags_syn", "flags_fin", "flags_str","win_size", "checksum", "checksum_status",
        "urgent_pointer", "stream", "proto_type", "proto_size", "hw_type", "hw_size", "hw_opcode", "src_hw_mac",
        "dst_hw_mac"
                ]
    
    df = pd.DataFrame(columns=col_names)
    first = 1
    for packet in cap.sniff_continuously():
        # print("df    --- %s seconds ---" % (time.time() - start))
        date_time = str(packet.sniff_time)
        # check if TCP layer exist in the i'th packet


        if "TCP" in packet:
            time_relative = float(packet.tcp.time_relative)
            srcport = int(packet.tcp.srcport)
            dstport = int(packet.tcp.dstport)
            data_len = int(packet.tcp.len)
            tcp_seq = int(packet.tcp.seq)
            tcp_seq_raw = int(packet.tcp.seq_raw)
            tcp_nxtseq = int(packet.tcp.nxtseq)
            tcp_ack = int(packet.tcp.ack)
            tcp_ack_raw = int(packet.tcp.ack_raw)
            tcp_flags = str(packet.tcp.flags) #hex
            tcp_flags_res = int(packet.tcp.flags_res)
            tcp_flags_ns = int(packet.tcp.flags_ns)
            tcp_flags_cwr = int(packet.tcp.flags_cwr)
            tcp_flags_ecn = int(packet.tcp.flags_ecn)
            tcp_flags_urg = int(packet.tcp.flags_urg)
            tcp_flags_ack = int(packet.tcp.flags_ack)
            tcp_flags_push = int(packet.tcp.flags_push)
            tcp_flags_reset = int(packet.tcp.flags_reset)
            tcp_flags_syn = int(packet.tcp.flags_syn)
            tcp_flags_fin = int(packet.tcp.flags_fin)
            tcp_flags_str = str(packet.tcp.flags_str)
            window_size = int(packet.tcp.window_size)
            checksum = str(packet.tcp.checksum) #hex
            checksum_status = int(packet.tcp.checksum_status)
            urgent_pointer = int(packet.tcp.urgent_pointer)
            stream = int(packet.tcp.stream)
            proto_name = str(packet.tcp.layer_name)

        # check if UDP layer exist in the i'th packet        
        elif "UDP" in packet:
            time_relative = float(packet.udp.time_relative)
            srcport = int(packet.udp.srcport)
            dstport = int(packet.udp.dstport)
            data_len = int(packet.udp.length)
            stream = int(packet.udp.stream)
            proto_name = str(packet.udp.layer_name)
            checksum = str(packet.udp.checksum) #hex
            checksum_status = int(packet.udp.checksum_status)
            tcp_seq = tcp_seq_raw = tcp_nxtseq = tcp_ack = tcp_ack_raw = tcp_flags = tcp_flags_res = tcp_flags_ns = tcp_flags_cwr = tcp_flags_ecn = tcp_flags_urg = tcp_flags_ack = tcp_flags_push = tcp_flags_reset = tcp_flags_syn = tcp_flags_fin = tcp_flags_str = window_size_value = window_size = urgent_pointer = None
        # check if both TCP and UDP layers do not exist in the i'th packet assign None to related objects
        else:   
            time_relative = srcport = dstport = data_len = tcp_seq = tcp_seq_raw = tcp_nxtseq = tcp_ack = tcp_ack_raw = tcp_flags = tcp_flags_res = tcp_flags_ns = tcp_flags_cwr = tcp_flags_ecn = tcp_flags_urg = tcp_flags_ack = tcp_flags_push = tcp_flags_reset = tcp_flags_syn = tcp_flags_fin = tcp_flags_str = window_size_value = window_size = checksum = checksum_status = urgent_pointer = proto_name = stream = None
          

        # check if IP (ipv4) layer exist in the i'th packet
        if  "IP" in packet:
            ip_src = str(packet.ip.src)
            ip_dst = str(packet.ip.dst)
            ip_proto = int(packet.ip.proto)
            ip_dsfield = str(packet.ip.dsfield) #hex
            ip_flags = str(packet.ip.flags) #hex
            ip_version = int(packet.ip.version)
        # check if IPV6 layer exist in the i'th packet
        elif "IPV6" in packet:
            ip_src = str(packet.ipv6.src)
            ip_dst = str(packet.ipv6.dst)
            ip_version = int(packet.ipv6.version)
            ip_proto = ip_dsfield = ip_flags = None
        # check if both IP (ipv4) and IPV6 layers do not exist in the i'th packet assign None to related objects
        else:
             ip_src = ip_dst = ip_proto =  ip_dsfield = ip_flags =  ip_version = None    
    
        # check if ARP layer exist in the i'th packet        
        if "ARP" in packet:
            proto_type = str(packet.arp.proto_type) #hex
            proto_size = int(packet.arp.proto_size)
            hw_type = int(packet.arp.hw_type)
            hw_size = int(packet.arp.hw_size)
            hw_opcode = int(packet.arp.opcode)
            src_hw_mac = str(packet.arp.src_hw_mac)
            ip_src = str(packet.arp.src_proto_ipv4)
            dst_hw_mac = str(packet.arp.dst_hw_mac)
            ip_dst = str(packet.arp.dst_proto_ipv4)
            proto_name = str(packet.arp.layer_name)
            ip_proto = 4
        else:
            proto_type = proto_size = hw_type = hw_size = hw_opcode = src_hw_mac = dst_hw_mac = None

        if first == 1:
            prev_time = float(packet.sniff_timestamp)
            first = 0

        duration = float(packet.sniff_timestamp) - prev_time
        pkt_length = int(packet.length)

        # adding the i'th packets information to the i'th row at the dataframe
        df.loc[0] = [
            date_time, time_relative, duration, ip_src, ip_dst, ip_proto, proto_name,
            pkt_length, ip_dsfield, ip_flags, ip_version, srcport, dstport,
            data_len, tcp_seq, tcp_seq_raw, tcp_nxtseq, tcp_ack, tcp_ack_raw, tcp_flags, tcp_flags_res,
            tcp_flags_ns,  tcp_flags_cwr,  tcp_flags_ecn, tcp_flags_urg, tcp_flags_ack, tcp_flags_push, tcp_flags_reset,
            tcp_flags_syn,  tcp_flags_fin,  tcp_flags_str, window_size,
            checksum, checksum_status, urgent_pointer, stream,  proto_type, proto_size, hw_type, hw_size, hw_opcode,
            src_hw_mac, dst_hw_mac
                    ]

        prev_time = float(packet.sniff_timestamp)
        p.send_stream(topic="Device1", value=df)
        # print(packet)

