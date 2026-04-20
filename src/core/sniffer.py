"""
Packet sniffer core
"""
from scapy.all import sniff
import threading

from src.parsers.dot11 import extract_mac, extract_ssid, extract_client_mac, extract_target_mac, is_probe_request, is_probe_response, is_beacon
from src.parsers.http import is_http, parse_http
from src.storage.devices import add_or_update_device
from src.storage.probe_store import add_probe_data
from src.storage.http_store import add_http_data
from src.core.channel import get_current_channel

sniffing_active = True
http_enabled = True
mac_enabled = True
prob_enabled = False
packet_count = 0
packet_count_lock = threading.Lock()

def init_sniffer_state():
    global sniffing_active, packet_count
    sniffing_active = True
    with packet_count_lock:
        packet_count = 0

def set_http_enabled(enabled):
    global http_enabled
    http_enabled = enabled

def set_mac_enabled(enabled):
    global mac_enabled
    mac_enabled = enabled

def set_prob_enabled(enabled):
    global prob_enabled
    prob_enabled = enabled

def stop_sniffing():
    global sniffing_active
    sniffing_active = False

def get_http_data():
    from src.storage.http_store import get_http_data as get_data
    return get_data()

def increment_packet_count():
    with packet_count_lock:
        global packet_count
        packet_count += 1
        return packet_count

def get_packet_count():
    with packet_count_lock:
        return packet_count

def pktHandler(pkt):
    try:
        count = increment_packet_count()
        if count % 1000 == 0:
            print(f"\n[STATS] Total packets: {count}")
        
        mac = extract_mac(pkt)
        if not mac:
            return
        
        current_ch = get_current_channel()
        
        if mac_enabled:
            add_or_update_device(mac, current_ch, False, "")
            if is_probe_request(pkt):
                ssid = extract_ssid(pkt)
                if ssid:
                    add_or_update_device(mac, current_ch, False, ssid)
            elif is_beacon(pkt):
                ssid = extract_ssid(pkt)
                if ssid:
                    add_or_update_device(mac, current_ch, True, ssid)
        
        if prob_enabled:
            if is_probe_request(pkt):
                ssid = extract_ssid(pkt)
                client_mac = extract_client_mac(pkt)
                target_mac = extract_target_mac(pkt)
                add_probe_data(client_mac, target_mac, ssid, current_ch, "request")
            elif is_probe_response(pkt):
                ssid = extract_ssid(pkt)
                ap_mac = extract_mac(pkt)
                client_mac = pkt.addr1 if pkt.addr1 else None
                add_probe_data(client_mac, ap_mac, ssid, current_ch, "response")
        
        if http_enabled and is_http(pkt):
            http_info = parse_http(pkt, current_ch)
            if http_info:
                add_http_data(http_info)
        
    except Exception:
        pass

def start_sniffing(iface_mon):
    print(f"[*] Starting packet capture on {iface_mon}...")
    sniff(iface=iface_mon, prn=pktHandler, store=False, filter="type mgt or type data")
