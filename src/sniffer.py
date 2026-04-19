"""
Packet sniffer and handler.
Captures 802.11 frames and processes probe requests and beacons.
"""
from scapy.all import sniff
from parser import extract_mac, extract_ssid, is_probe_request, is_beacon
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
                
    except Exception:
        pass

def start_sniffing(iface_mon):
    sniff(iface=iface_mon, prn=pktHandler, store=False)
