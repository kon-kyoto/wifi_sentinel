"""
Packet sniffer and handler.
Captures 802.11 frames and processes probe requests and beacons.
"""
from scapy.all import sniff

from parser import extract_mac, extract_ssid, is_probe_request, is_beacon
from http_parser  import is_http, parse_http
from storage import add_or_update_device
from channel import get_current_channel

sniffing_active = True

def init_sniffer_state():
    global sniffing_active
    sniffing_active = True

def stop_sniffing():
    global sniffing_active
    sniffing_active = False

def pktHandler(pkt):
    try:
        mac = extract_mac(pkt)
        if not mac:
            return
        
        current_ch = get_current_channel()
        
        if is_probe_request(pkt):
            ssid = extract_ssid(pkt)
            if ssid:
                is_new_ssid = add_or_update_device(mac, current_ch, False, ssid)
                if is_new_ssid:
                    print(f"    [{mac}] Probing: {ssid}")
        
        elif is_beacon(pkt):
            ssid = extract_ssid(pkt)
            if ssid:
                add_or_update_device(mac, current_ch, True, ssid)

        if is_http(pkt):
            http_info = parse_http(pkt, get_current_channel())

            if http_info['type'] == 'request':
                print(f"\n[HTTP Request] {http_info['method']} {http_info['host']}{http_info['path']}")
                print(f"    From: {http_info['src_ip']}:{http_info['src_port']}")
            elif http_info['type'] == 'response':
                print(f"\n[HTTP Response] {http_info['status_code']} {http_info['reason']}")
                print(f"    Type: {http_info['content_type']}")
    except Exception:
        pass

def start_sniffing(iface_mon):
    sniff(iface=iface_mon, prn=pktHandler, store=False)
