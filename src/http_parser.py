"""
Packet HTTP parsing utilities.
Extracts HTTP request/response.
"""
from scapy.all import TCP, IP, Raw
from scapy.layers import http

def is_http(pkt):
    """Check if packet is HTTP traffic (ports 80, 8080, 8000)"""
    if pkt.haslayer(TCP):
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
        http_ports = [80, 8080, 8000, 8888]
        return sport in http_ports or dport in http_ports
    return False

def parse_http(pkt, current_channel, rssi=None):
    """Extract HTTP request/response information"""
    result = {
        'type': None,
        'channel': current_channel,
        'rssi': rssi,
        'src_ip': None,
        'dst_ip': None,
        'src_port': None,
        'dst_port': None
    }

    # IP addresses
    if pkt.haslayer(IP):
        result['src_ip'] = pkt[IP].src
        result['dst_ip'] = pkt[IP].dst
    
    # TCP ports
    if pkt.haslayer(TCP):
        result['src_port'] = pkt[TCP].sport
        result['dst_port'] = pkt[TCP].dport
    
    # HTTP Request — используем http.HTTPRequest
    if pkt.haslayer(http.HTTPRequest):
        result['type'] = 'request'
        req = pkt[http.HTTPRequest]
        result['method'] = req.Method.decode() if req.Method else None
        result['path'] = req.Path.decode() if req.Path else None
        result['host'] = req.Host.decode() if req.Host else None
        result['user_agent'] = req.User_Agent.decode() if req.User_Agent else None
        
        # Extract POST data if present
        if pkt.haslayer(Raw) and result['method'] == 'POST':
            try:
                result['post_data'] = pkt[Raw].load.decode('utf-8', errors='ignore')[:500]
            except:
                result['post_data'] = None
    
    # HTTP Response
    elif pkt.haslayer(http.HTTPResponse):
        result['type'] = 'response'
        resp = pkt[http.HTTPResponse]
        result['status_code'] = resp.Status_Code.decode() if resp.Status_Code else None
        result['reason'] = resp.Reason_Phrase.decode() if resp.Reason_Phrase else None
        result['content_type'] = resp.Content_Type.decode() if resp.Content_Type else None
    
    return result
