"""
Утилиты для парсинга HTTP пакетов.
Извлекает HTTP запросы и ответы.
"""
from scapy.all import TCP, IP, Raw
import scapy.layers.http as http
from scapy.layers.http import HTTPRequest, HTTPResponse

def is_http(pkt):
    if pkt.haslayer(TCP):
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
        http_ports = [80, 8080, 8000, 8888]
        return sport in http_ports or dport in http_ports
    return False

def parse_http(pkt, current_channel, rssi=None):
    result = {
        'type': None,
        'channel': current_channel,
        'rssi': rssi,
        'src_ip': None,
        'dst_ip': None,
        'src_port': None,
        'dst_port': None
    }

    if pkt.haslayer(IP):
        result['src_ip'] = pkt[IP].src
        result['dst_ip'] = pkt[IP].dst
    
    if pkt.haslayer(TCP):
        result['src_port'] = pkt[TCP].sport
        result['dst_port'] = pkt[TCP].dport
    
    if pkt.haslayer(HTTPRequest):
        result['type'] = 'request'
        req = pkt[HTTPRequest]
        result['method'] = req.Method.decode() if req.Method else None
        result['path'] = req.Path.decode() if req.Path else None
        result['host'] = req.Host.decode() if req.Host else None
        result['user_agent'] = req.User_Agent.decode() if req.User_Agent else None
        
        if pkt.haslayer(Raw) and result['method'] == 'POST':
            try:
                result['post_data'] = pkt[Raw].load.decode('utf-8', errors='ignore')[:500]
            except:
                result['post_data'] = None
    
    elif pkt.haslayer(HTTPResponse):
        result['type'] = 'response'
        resp = pkt[HTTPResponse]
        result['status_code'] = resp.Status_Code.decode() if resp.Status_Code else None
        result['reason'] = resp.Reason_Phrase.decode() if resp.Reason_Phrase else None
        result['content_type'] = resp.Content_Type.decode() if resp.Content_Type else None
    
    return result
