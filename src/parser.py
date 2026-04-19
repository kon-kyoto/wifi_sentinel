"""
Утилиты для парсинга пакетов.
Извлекает MAC-адреса, SSID и определяет типы пакетов из 802.11 кадров.
"""
from scapy.all import Dot11, Dot11ProbeReq, Dot11ProbeResp, Dot11Beacon, Dot11Elt

def extract_mac(pkt):
    if not pkt.haslayer(Dot11):
        return None
    mac = pkt.addr2 or pkt.addr3
    return str(mac).upper() if mac else None

def extract_client_mac(pkt):
    if not pkt.haslayer(Dot11):
        return None
    return str(pkt.addr2).upper() if pkt.addr2 else None

def extract_target_mac(pkt):
    if not pkt.haslayer(Dot11):
        return None
    return str(pkt.addr3).upper() if pkt.addr3 else None

def extract_ssid(pkt):
    try:
        elt = pkt.getlayer(Dot11Elt)
        while elt:
            if elt.ID == 0:
                return elt.info.decode('utf-8', errors='ignore')
            elt = elt.payload.getlayer(Dot11Elt)
    except:
        pass
    return ""

def is_probe_request(pkt):
    return pkt.haslayer(Dot11ProbeReq)

def is_probe_response(pkt):
    return pkt.haslayer(Dot11ProbeResp)

def is_beacon(pkt):
    return pkt.haslayer(Dot11Beacon)
