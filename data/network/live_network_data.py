"""
Implementation of the request and communication handler.
"""
import concurrent
import os
import time

import numpy as np
import pandas as pd
import pyshark


    # @param interface: the interface
    # @param timeout: time interval
def get_live_network_data(interface,packet_amount):
    # start = time.time()
    cap = pyshark.LiveCapture(interface=interface)
    cap.sniff(packet_amount)
    col_names = [
        "duration","source","destination","protocol","protocol_name","bytes","service","flag", "ip_vers" ,"src_port","dst_port","proto_len","seq","seq_raw","next_seq","ack","ack_raw"
        ,"tcp_flags","flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push", "flags_reset", "flags_syn", "flags_fin", "flags_str"
        ,"win","win_size","checksum","checksum_status","urgent_pointer", "stream" ,  "proto_type" , "proto_size" , "hw_type" , "hw_size" , "hw_opcode"
        ,"src_hw_mac" , "src_proto_ipv4" , "dst_hw_mac" , "dst_proto_ipv4"
                ]
    
    df = pd.DataFrame(columns = col_names) 
    total_length = len(cap)
    for i in range(total_length):
    
        # check if TCP layer exist in the i'th packet
        if "TCP" in cap[i]:
            time_relative =  cap[i].tcp.time_relative
            srcport = cap[i].tcp.srcport
            dstport = cap[i].tcp.dstport
            proto_len = cap[i].tcp.len
            tcp_seq = cap[i].tcp.seq
            tcp_seq_raw = cap[i].tcp.seq_raw
            tcp_nxtseq = cap[i].tcp.nxtseq
            tcp_ack = cap[i].tcp.ack
            tcp_ack_raw = cap[i].tcp.ack_raw
            tcp_flags = cap[i].tcp.flags
            tcp_flags_res =  cap[i].tcp.flags_res
            tcp_flags_ns = cap[i].tcp.flags_ns
            tcp_flags_cwr = cap[i].tcp.flags_cwr
            tcp_flags_ecn = cap[i].tcp.flags_ecn 
            tcp_flags_urg = cap[i].tcp.flags_urg
            tcp_flags_ack = cap[i].tcp.flags_ack
            tcp_flags_push =  cap[i].tcp.flags_push
            tcp_flags_reset = cap[i].tcp.flags_reset
            tcp_flags_syn = cap[i].tcp.flags_syn
            tcp_flags_fin = cap[i].tcp.flags_fin
            tcp_flags_str = cap[i].tcp.flags_str
            window_size_value = cap[i].tcp.window_size_value
            window_size = cap[i].tcp.window_size
            checksum =  cap[i].tcp.checksum 
            checksum_status =  cap[i].tcp.checksum_status
            urgent_pointer = cap[i].tcp.urgent_pointer
            stream = cap[i].tcp.stream
            proto_name = cap[i].tcp.layer_name

        # check if UDP layer exist in the i'th packet        
        elif "UDP" in cap[i]:
            time_relative =  cap[i].udp.time_relative
            srcport = cap[i].udp.srcport
            dstport = cap[i].udp.dstport
            proto_len = cap[i].udp.length
            stream = cap[i].udp.stream
            proto_name = cap[i].udp.layer_name
            checksum =  cap[i].udp.checksum 
            checksum_status =  cap[i].udp.checksum_status
            tcp_seq = tcp_seq_raw= tcp_nxtseq =tcp_ack= tcp_ack_raw = tcp_flags = tcp_flags_res = tcp_flags_ns =  tcp_flags_cwr  =  tcp_flags_ecn = tcp_flags_urg  = tcp_flags_ack = tcp_flags_push = tcp_flags_reset   = tcp_flags_syn  =  tcp_flags_fin  =  tcp_flags_str  = window_size_value = window_size  =  urgent_pointer = None

        # check if both TCP and UDP layers do not exist in the i'th packet assign None to related objects
        else:   
            time_relative = srcport = dstport = proto_len= tcp_seq = tcp_seq_raw= tcp_nxtseq =tcp_ack= tcp_ack_raw = tcp_flags = tcp_flags_res = tcp_flags_ns =  tcp_flags_cwr  =  tcp_flags_ecn = tcp_flags_urg  = tcp_flags_ack = tcp_flags_push = tcp_flags_reset   = tcp_flags_syn  =  tcp_flags_fin  =  tcp_flags_str  = window_size_value = window_size  = checksum = checksum_status = urgent_pointer = proto_name =  stream = None
          
        # check if IP (ipv4) layer exist in the i'th packet        
        if  "IP" in cap[i]:  
            ip_src = cap[i].ip.src
            ip_dst = cap[i].ip.dst
            ip_proto  = cap[i].ip.proto 
            ip_dsfield = cap[i].ip.dsfield
            ip_flags = cap[i].ip.flags
            ip_version = cap[i].ip.version

        # check if IPV6 layer exist in the i'th packet        
        elif "IPV6" in cap[i]:  
            ip_src = cap[i].ipv6.src
            ip_dst = cap[i].ipv6.dst
            ip_version = cap[i].ipv6.version
            ip_proto = ip_dsfield = ip_flags = None

        # check if both IP (ipv4) and IPV6 layers do not exist in the i'th packet assign None to related objects
        else:
             ip_src = ip_dst = ip_proto =  ip_dsfield = ip_flags =  ip_version = None    

        # check if ARP layer exist in the i'th packet        
        if "ARP" in cap[i]:
            proto_type = cap[i].arp.proto_type
            proto_size = cap[i].arp.proto_size
            hw_type = cap[i].arp.hw_type
            hw_size = cap[i].arp.hw_size
            hw_opcode = cap[i].arp.opcode
            src_hw_mac = cap[i].arp.src_hw_mac
            src_proto_ipv4 = cap[i].arp.src_proto_ipv4
            dst_hw_mac = cap[i].arp.dst_hw_mac
            dst_proto_ipv4 =  cap[i].arp.dst_proto_ipv4
        else:
            proto_type = proto_size = hw_type = hw_size =hw_opcode = src_hw_mac = src_proto_ipv4 = dst_hw_mac = dst_proto_ipv4 = None

        # adding the i'th packets information to the i'th row at the dataframe
        df.loc[i] = [
            time_relative , ip_src , ip_dst , ip_proto, proto_name 
            , cap[i].length , ip_dsfield , ip_flags , ip_version ,  srcport , dstport 
            , proto_len, tcp_seq , tcp_seq_raw, tcp_nxtseq ,tcp_ack, tcp_ack_raw , tcp_flags , tcp_flags_res
            , tcp_flags_ns ,  tcp_flags_cwr  ,  tcp_flags_ecn , tcp_flags_urg  , tcp_flags_ack , tcp_flags_push , tcp_flags_reset 
            , tcp_flags_syn  ,  tcp_flags_fin  ,  tcp_flags_str  , window_size_value , window_size
            , checksum , checksum_status , urgent_pointer , stream ,  proto_type , proto_size , hw_type , hw_size ,hw_opcode 
            , src_hw_mac , src_proto_ipv4 , dst_hw_mac , dst_proto_ipv4
                    ]
    
    return df


# if __name__ == "__main__":
#     df = get_live_network_data("Wi-Fi",5)
#     print(df)