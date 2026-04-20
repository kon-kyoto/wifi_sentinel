"""
HTTP data storage
"""
import csv
import os
from threading import Lock

http_data_list = []
http_data_lock = Lock()

def add_http_data(data):
    with http_data_lock:
        http_data_list.append(data)

def get_http_data():
    with http_data_lock:
        return http_data_list.copy()

def save_http_to_csv(write_prefix, http_data):
    if not write_prefix or not http_data:
        return
    
    http_filename = f"{write_prefix}_http.csv"
    mode = 'a' if os.path.exists(http_filename) else 'w'
    
    with open(http_filename, mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if mode == 'w':
            writer.writerow(['timestamp', 'src_ip', 'dst_ip', 'src_port', 'dst_port', 
                           'method', 'host', 'path', 'user_agent', 'post_data', 
                           'status_code', 'reason', 'content_type', 'channel'])
        
        for data in http_data:
            writer.writerow([
                data.get('timestamp', ''),
                data.get('src_ip', ''),
                data.get('dst_ip', ''),
                data.get('src_port', ''),
                data.get('dst_port', ''),
                data.get('method', ''),
                data.get('host', ''),
                data.get('path', ''),
                data.get('user_agent', ''),
                data.get('post_data', ''),
                data.get('status_code', ''),
                data.get('reason', ''),
                data.get('content_type', ''),
                data.get('channel', '')
            ])
    
    print(f"[+] Saved {len(http_data)} HTTP entries to {http_filename}")
