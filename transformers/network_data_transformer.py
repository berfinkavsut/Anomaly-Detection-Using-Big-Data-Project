
import ipaddress
import re
import pandas as pd



def network_data_transformer(df):
    data = df.iloc[[0]]
    col_names = [
        "time", "duration", "source_ip", "destination_ip", "protocol", "bytes","dif_serv",
        "flag", "ip_vers", "src_port", "dst_port", "proto_len", "seq", "seq_raw", "next_seq", "ack", "ack_raw",
        "tcp_flags", "flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push",
        "flags_reset", "flags_syn", "flags_fin", "flags_str", "win", "win_size", "checksum", "checksum_status",
        "urgent_pointer", "stream", "proto_type", "proto_size", "hw_type", "hw_size", "hw_opcode", "src_hw_mac",
        "dst_hw_mac"
    ]
    new_Data = pd.DataFrame(columns=col_names)

    max_port = 65535
    max_ip = 2 ** 32 - 1
    max_ipv6 = 2 ** 64 - 1
    max_seq_raw = 2 ** 32 - 1
    max_mac = 2 ** 48 - 1
    # if data["ip_vers"].values == 6:
    #     max_ip = max_ipv6
    # nf.drop(["date&time","protocol_name" ], inplace = True , axis=1)
    #
    # new_data.drop(["date&time","protocol_name" ], inplace = True ,axis=0)

    # new_data["dif_serv"] = int(data.iloc[0]["dif_serv"], 16)
    # new_data["flag"] = int(data.iloc[0]["flag"], 16)

    # new_data = new_data.drop(["ack_raw","seq_raw, flags_str" ], axis=1)
    # if data.iloc[0]["tcp_flags"] == None:
    #     new_data["tcp_flags"] = 0
    # else:
    #     new_data["tcp_flags"] = int(data.iloc[0]["tcp_flags"], 16) #None geliyorDS
    #
    # new_data["checksum"] = int(data.iloc[0]["checksum"], 16)
    # new_data["proto_type"] = int(data.iloc[0]["proto_type"], 16)
    # new_data["src_hw_mac"] = mac_to_int(data.iloc[0]["src_hw_mac"]) / max_mac
    # new_data["dst_hw_mac"] = mac_to_int(data.iloc[0]["dst_hw_mac"]) / max_mac


    time_relative = data.iloc[0]["time"]
    duration = data.iloc[0]["duration"]
    ip_src = int(ipaddress.ip_address(data.iloc[0]["source_ip"])) / max_ip
    ip_dst = int(ipaddress.ip_address(data.iloc[0]["destination_ip"])) / max_ip
    ip_proto = data.iloc[0]["protocol"]
    packet_length = data.iloc[0]["bytes"]
    ip_dsfield = int(data.iloc[0]["dif_serv"], 16)
    ip_flags =int(data.iloc[0]["flag"], 16)
    ip_version = data.iloc[0]["ip_vers"]
    srcport = data.iloc[0]["src_port"] / max_port
    dstport = data.iloc[0]["dst_port"] / max_port
    proto_len = data.iloc[0]["proto_len"]
    tcp_seq = data.iloc[0]["seq"]
    tcp_seq_raw = data.iloc[0]["seq_raw"]
    tcp_nxtseq = data.iloc[0]["next_seq"]
    tcp_ack = data.iloc[0]["ack"]
    tcp_ack_raw = data.iloc[0]["ack_raw"]
    tcp_flags = data.iloc[0]["tcp_flags"]
    tcp_flags_res = data.iloc[0]["flags_res"]
    tcp_flags_ns = data.iloc[0]["flags_ns"]
    tcp_flags_cwr = data.iloc[0]["flags_cwr"]
    tcp_flags_ecn = data.iloc[0]["flags_ecn"]
    tcp_flags_urg = data.iloc[0]["flags_urg"]
    tcp_flags_ack = data.iloc[0]["flags_ack"]
    tcp_flags_push = data.iloc[0]["flags_push"]
    tcp_flags_reset = data.iloc[0]["flags_reset"]
    tcp_flags_syn = data.iloc[0]["flags_syn"]
    tcp_flags_fin = data.iloc[0]["flags_fin"]
    tcp_flags_str = data.iloc[0]["flags_str"]
    window_size_value = data.iloc[0]["win"]
    window_size = data.iloc[0]["win_size"]
    checksum = data.iloc[0]["checksum"]
    checksum_status = data.iloc[0]["checksum_status"]
    urgent_pointer = data.iloc[0]["urgent_pointer"]
    stream = data.iloc[0]["stream"]
    proto_type = data.iloc[0]["proto_type"]
    proto_size = data.iloc[0]["proto_size"]
    hw_type = data.iloc[0]["hw_type"]
    hw_size = data.iloc[0]["hw_size"]
    hw_opcode= data.iloc[0]["hw_opcode"]
    src_hw_mac = data.iloc[0]["src_hw_mac"]
    dst_hw_mac = data.iloc[0]["dst_hw_mac"]


    new_Data.loc[0] = [
        time_relative, duration, ip_src, ip_dst, ip_proto,
        packet_length.length, ip_dsfield, ip_flags, ip_version, srcport, dstport,
        proto_len, tcp_seq, tcp_seq_raw, tcp_nxtseq, tcp_ack, tcp_ack_raw, tcp_flags, tcp_flags_res,
        tcp_flags_ns, tcp_flags_cwr, tcp_flags_ecn, tcp_flags_urg, tcp_flags_ack, tcp_flags_push, tcp_flags_reset,
        tcp_flags_syn, tcp_flags_fin, tcp_flags_str, window_size_value, window_size,
        checksum, checksum_status, urgent_pointer, stream, proto_type, proto_size, hw_type, hw_size, hw_opcode,
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
