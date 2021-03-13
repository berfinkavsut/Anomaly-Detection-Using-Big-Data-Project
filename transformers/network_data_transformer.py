
import ipaddress
import re

# col_names = [
#     "date&time", "time", "duration", "source_ip", "destination_ip", "protocol", "protocol_name", "bytes", "service",
#     "flag", "ip_vers", "src_port", "dst_port", "proto_len", "seq", "seq_raw", "next_seq", "ack", "ack_raw",
#     "tcp_flags", "flags_res", "flags_ns", "flags_cwr", "flags_ecn", "flags_urg", "flags_ack", "flags_push",
#     "flags_reset", "flags_syn", "flags_fin", "flags_str", "win", "win_size", "checksum", "checksum_status",
#     "urgent_pointer", "stream", "proto_type", "proto_size", "hw_type", "hw_size", "hw_opcode", "src_hw_mac",
#     "dst_hw_mac"
# ]


def network_data_transformer(data):
    max_port = 65535
    max_ip = 2 ** 32 - 1
    max_ipv6 = 2 ** 64 - 1
    max_seq_raw = 2 ** 32 - 1
    max_mac = 2 ** 48 - 1

    if data["ip_vers"].values == 6:
        max_ip = max_ipv6
    new_data = data
    new_data = new_data.drop(["date&time","protocol_name" ], axis=1)
    new_data["source_ip"] = int(ipaddress.ip_address(data["source_ip"])) / max_ip
    new_data["destination_ip"] = int(ipaddress.ip_address(data["destination_ip"])) / max_ip
    new_data["service"] = int(data["service"], 16)
    new_data["flag"] = int(data["flag"], 16)
    new_data["src_port"] = data["src_port"] / max_port
    new_data["dst_port"] = data["dst_port"] / max_port
    # new_data = new_data.drop(["ack_raw","seq_raw, flags_str" ], axis=1)
    new_data["tcp_flags"] = int(data["tcp_flags"], 16)
    new_data["checksum"] = int(data["checksum"], 16)
    new_data["proto_type"] = int(data["proto_type"], 16)
    new_data["src_hw_mac"] = mac_to_int(data["src_hw_mac"]) / max_mac
    new_data["dst_hw_mac"] = mac_to_int(data["dst_hw_mac"]) / max_mac
    # Nonelar bakilacak



    return new_data


def mac_to_int(mac):
    res = re.match('^((?:(?:[0-9a-f]{2}):){5}[0-9a-f]{2})$', mac.lower())
    if res is None:
        raise ValueError('invalid mac address')
    return int(res.group(0).replace(':', ''), 16)


if __name__ == "__main__":
    mac_str = "00:1B:44:11:3A:B7"
    print(mac_to_int(mac_str))
