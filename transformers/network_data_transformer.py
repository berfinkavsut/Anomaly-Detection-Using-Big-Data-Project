
import ipaddress
import re
import pandas as pd


"""IMPORTANT!!!
    checksum_status possible values
    urgent_pointer
    ip_flag
    ipv6 max too large
    
"""


def network_data_transformer(df):
    data = df.iloc[[0]]
    col_names = [
        "time", "duration", "source_ip", "destination_ip", "protocol", "packet_len","dif_serv",
        "flag", "ip_vers", "src_port", "dst_port", "data_len", "seq", "seq_raw", "next_seq", "ack", "ack_raw",
        "flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push",
        "flags_reset", "flags_syn", "flags_fin", "win_size", "checksum", "checksum_status",
        "urgent_pointer", "proto_type", "proto_size", "hw_type", "hw_size", "hw_opcode", "src_hw_mac",
        "dst_hw_mac"
    ]
    new_Data = pd.DataFrame(columns=col_names)

    max_port = 65535
    max_ip = 2 ** 32 - 1
    max_ipv6 = 2 ** 128 - 1
    max_seq_raw = 2 ** 32 - 1
    max_ack_raw = 2 ** 32 - 1
    max_checksum = 2 ** 16 -1
    max_win_size = 65535
    max_packet_length = 65535
    max_proto_no = 255
    max_mac_adr = 2 ** 48 - 1

    # new_data.drop(["date&time","protocol_name" ], inplace = True ,axis=0)
    # new_data = new_data.drop(["ack_raw","seq_raw, flags_str" ], axis=1)

    time_relative = data.iloc[0]["time"]
    duration = data.iloc[0]["duration"]

    if data.iloc[0]["ip_vers"] == 6:
        max_ip = max_ipv6

    if data.iloc[0]["source_ip"] is None:
        ip_src = 0
    else:
        ip_src = int(ipaddress.ip_address(data.iloc[0]["source_ip"])) / max_ip

    if data.iloc[0]["destination_ip"] is None:
        ip_dst = 0
    else:
        ip_dst = int(ipaddress.ip_address(data.iloc[0]["destination_ip"])) / max_ip

    if data.iloc[0]["protocol"] is None:
        ip_proto = 0
    else:
        ip_proto = data.iloc[0]["protocol"] / max_proto_no

    packet_length = data.iloc[0]["packet_len"] / max_packet_length

    if data.iloc[0]["dif_serv"] is None:
        ip_dsfield = 0
    else:
        ip_dsfield = int(data.iloc[0]["dif_serv"], 16)

    if data.iloc[0]["flag"] is None:
        ip_flags = 4  # if ARP
    else:
        ip_flags =int(data.iloc[0]["flag"], 16)

    if data.iloc[0]["ip_vers"] is None:
        ip_version = 0
    else:
        ip_version = data.iloc[0]["ip_vers"] / 6

    if data.iloc[0]["src_port"] is None:
        srcport = 0
    else:
        srcport = data.iloc[0]["src_port"] / max_port

    if data.iloc[0]["dst_port"] is None:
        dstport = 0
    else:
        dstport = data.iloc[0]["dst_port"] / max_port

    if data.iloc[0]["data_len"] is None:
        data_len = 0
    else:
        data_len = data.iloc[0]["data_len"] / max_packet_length

    if  data.iloc[0]["seq"] is None:
        tcp_seq = 0
    else:
        tcp_seq = data.iloc[0]["seq"] / max_seq_raw

    if data.iloc[0]["seq_raw"] is None:
        tcp_seq_raw = 0
    else:
        tcp_seq_raw = data.iloc[0]["seq_raw"] / max_seq_raw

    if data.iloc[0]["next_seq"] is None:
        tcp_nxtseq = 0
    else:
        tcp_nxtseq = data.iloc[0]["next_seq"] / max_seq_raw

    if data.iloc[0]["ack"] is None:
        tcp_ack = 0
    else:
        tcp_ack = data.iloc[0]["ack"]  / max_ack_raw

    if data.iloc[0]["ack_raw"] is None:
        tcp_ack_raw = 0
    else:
        tcp_ack_raw = data.iloc[0]["ack_raw"] / max_ack_raw

    if data.iloc[0]["flags_res"] is None:
        tcp_flags_res = 0.5
    else:
        tcp_flags_res = data.iloc[0]["flags_res"]

    if data.iloc[0]["flags_ns"] is None:
        tcp_flags_ns = 0.5
    else:
        tcp_flags_ns = data.iloc[0]["flags_ns"]

    if data.iloc[0]["flags_cwr"] is None:
        tcp_flags_cwr = 0.5
    else:
        tcp_flags_cwr = data.iloc[0]["flags_cwr"]

    if data.iloc[0]["flags_ecn"] is None:
        tcp_flags_ecn = 0.5
    else:
        tcp_flags_ecn = data.iloc[0]["flags_ecn"]

    if data.iloc[0]["flags_urg"] is None:
        tcp_flags_urg = 0.5
    else:
        tcp_flags_urg = data.iloc[0]["flags_urg"]
    if data.iloc[0]["flags_ack"] is None:
        tcp_flags_ack = 0.5
    else:
        tcp_flags_ack = data.iloc[0]["flags_ack"]
    if data.iloc[0]["flags_push"] is None:
        tcp_flags_push = 0.5
    else:
        tcp_flags_push = data.iloc[0]["flags_push"]

    if data.iloc[0]["flags_reset"] is None:
        tcp_flags_reset = 0.5
    else:
        tcp_flags_reset = data.iloc[0]["flags_reset"]

    if data.iloc[0]["flags_syn"] is None:
        tcp_flags_syn = 0.5
    else:
        tcp_flags_syn = data.iloc[0]["flags_syn"]

    if data.iloc[0]["flags_fin"] is None:
        tcp_flags_fin =0.5
    else:
        tcp_flags_fin = data.iloc[0]["flags_fin"]

    if data.iloc[0]["win_size"] is None:
        window_size = 0
    else:
        window_size = data.iloc[0]["win_size"] / max_win_size

    if data.iloc[0]["checksum"] is None:
        checksum = 0
    else:
        checksum = int(data.iloc[0]["checksum"], 16) / max_checksum

    if data.iloc[0]["checksum_status"] is None:
        checksum_status = 0
    else:
        checksum_status = data.iloc[0]["checksum_status"]

    if data.iloc[0]["urgent_pointer"] is None:
        urgent_pointer = 0.5
    else:
        urgent_pointer = data.iloc[0]["urgent_pointer"]

    if data.iloc[0]["proto_type"] is None:
        proto_type =0
    else:
        proto_type = int(data.iloc[0]["proto_type"], 16)

    if data.iloc[0]["proto_size"] is None:
        proto_size = 0
    else:
        proto_size = data.iloc[0]["proto_size"]

    if data.iloc[0]["hw_type"] is None:
        hw_type = 0
    else:
        hw_type = data.iloc[0]["hw_type"]

    if data.iloc[0]["hw_size"] is None:
        hw_size = 0
    else:
        hw_size = data.iloc[0]["hw_size"]

    if data.iloc[0]["hw_opcode"] is None:
        hw_opcode = 0
    else:
        hw_opcode= data.iloc[0]["hw_opcode"]

    if data.iloc[0]["src_hw_mac"] is None:
        src_hw_mac = 0
    else:
        src_hw_mac = mac_to_int(data.iloc[0]["src_hw_mac"]) / max_mac_adr

    if data.iloc[0]["dst_hw_mac"] is None:
        dst_hw_mac = 0
    else:
        dst_hw_mac = mac_to_int(data.iloc[0]["dst_hw_mac"]) / max_mac_adr

    new_Data.loc[0] = [
        time_relative, duration, ip_src, ip_dst, ip_proto,
        packet_length, ip_dsfield, ip_flags, ip_version, srcport, dstport,
        data_len, tcp_seq, tcp_seq_raw, tcp_nxtseq, tcp_ack, tcp_ack_raw, tcp_flags_res,
        tcp_flags_ns, tcp_flags_cwr, tcp_flags_ecn, tcp_flags_urg, tcp_flags_ack, tcp_flags_push, tcp_flags_reset,
        tcp_flags_syn, tcp_flags_fin, window_size,
        checksum, checksum_status, urgent_pointer, proto_type, proto_size, hw_type, hw_size, hw_opcode,
        src_hw_mac, dst_hw_mac
                ]

    return new_Data


def mac_to_int(mac):
    res = re.match('^((?:(?:[0-9a-f]{2}):){5}[0-9a-f]{2})$', mac.lower())
    if res is None:
        raise ValueError('invalid mac address')
    return int(res.group(0).replace(':', ''), 16)


if __name__ == "__main__":
    mac_str = "00:1B:44:11:3A:B7"
    print(mac_to_int(mac_str))
