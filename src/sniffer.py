"""
Сниффер и обработчик пакетов.
Захватывает 802.11 кадры и обрабатывает probe запросы и beacon кадры.
"""
from scapy.all import sniff
import threading

from parser import extract_mac, extract_ssid, is_probe_request, is_beacon
from http_parser import is_http, parse_http
from storage import add_or_update_device
from channel import get_current_channel

sniffing_active = True
http_enabled = True
mac_enabled = True
packet_count = 0
packet_count_lock = threading.Lock()
http_data_list = []
http_data_lock = threading.Lock()

def init_sniffer_state():
    global sniffing_active, packet_count, http_data_list
    sniffing_active = True
    with packet_count_lock:
        packet_count = 0
    with http_data_lock:
        http_data_list = []

def set_http_enabled(enabled):
    global http_enabled
    http_enabled = enabled

def set_mac_enabled(enabled):
    global mac_enabled
    mac_enabled = enabled

def stop_sniffing():
    global sniffing_active
    sniffing_active = False

def get_http_data():
    with http_data_lock:
        return http_data_list.copy()

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
        
        if http_enabled and is_http(pkt):
            http_info = parse_http(pkt, current_ch)
            if http_info and http_info.get('type') == 'request':
                with http_data_lock:
                    http_data_list.append(http_info)
                print(f"\n[HTTP Request] {http_info.get('method', '?')} {http_info.get('host', '?')}{http_info.get('path', '?')}")
                print(f"    From: {http_info.get('src_ip', '?')}:{http_info.get('src_port', '?')}")
                if http_info.get('user_agent'):
                    print(f"    User-Agent: {http_info['user_agent'][:100]}")
            elif http_info and http_info.get('type') == 'response':
                print(f"\n[HTTP Response] {http_info.get('status_code', '?')} {http_info.get('reason', '?')}")
                print(f"    Content-Type: {http_info.get('content_type', '?')}")
        
    except Exception:
        pass

def start_sniffing(iface_mon):
    print(f"[*] Starting packet capture on {iface_mon}...")
    sniff(iface=iface_mon, prn=pktHandler, store=False, filter="type mgt or type data")
