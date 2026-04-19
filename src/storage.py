"""
Управление хранением устройств.
Хранит обнаруженные устройства и сохраняет их в CSV файл.
"""
import csv
import os
from threading import Lock

devices = {}
devices_lock = Lock()
known_macs = set()

def load_existing_devices(write_prefix):
    global known_macs, devices
    mac_filename = f"{write_prefix}_mac.csv"
    
    if not os.path.exists(mac_filename):
        print(f"[ ] No existing database found, creating new one")
        return
    
    try:
        with open(mac_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                mac = row['mac']
                known_macs.add(mac)
                if mac not in devices:
                    devices[mac] = {
                        'essid': row['essid'],
                        'channel': int(row['channel']),
                        'is_ap': row['is_ap'] == 'YES'
                    }
        print(f"[+] Loaded {len(known_macs)} existing devices from {mac_filename}")
    except Exception as e:
        print(f"[-] Failed to load existing devices: {e}")

def add_or_update_device(mac, channel, is_ap=False, ssid=""):
    with devices_lock:
        global known_macs
        
        is_new_mac = mac not in known_macs
        
        if is_new_mac:
            known_macs.add(mac)
            print(f"[+] NEW\tMAC: {mac}\tChannel: {channel}")
        
        if mac not in devices:
            devices[mac] = {
                'essid': "",
                'channel': channel,
                'is_ap': False
            }
        else:
            if devices[mac]['channel'] != channel:
                devices[mac]['channel'] = channel
        
        if is_ap:
            devices[mac]['is_ap'] = True
        
        if ssid and ssid not in devices[mac]['essid']:
            if devices[mac]['essid']:
                devices[mac]['essid'] += f", {ssid}"
            else:
                devices[mac]['essid'] = ssid
            print(f"    [{mac}] Probing: {ssid}")
            return True
        return False

def save_to_csv(write_prefix):
    if not write_prefix:
        return
    
    with devices_lock:
        if not devices:
            return
        
        mac_filename = f"{write_prefix}_mac.csv"
        
        with open(mac_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['mac', 'essid', 'channel', 'is_ap'])
            
            for mac, info in devices.items():
                writer.writerow([
                    mac,
                    info['essid'] if info['essid'] else "",
                    info['channel'],
                    "YES" if info['is_ap'] else "NO"
                ])
        
        print(f"\n[+] Saved {len(devices)} devices to {mac_filename}")

def save_http_to_csv(write_prefix, http_data):
    if not write_prefix or not http_data:
        return
    
    http_filename = f"{write_prefix}_http.csv"
    mode = 'a' if os.path.exists(http_filename) else 'w'
    
    with open(http_filename, mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if mode == 'w':
            writer.writerow(['src_ip', 'dst_ip', 'method', 'host', 'path', 'user_agent', 'channel'])
        
        for data in http_data:
            writer.writerow([
                data.get('src_ip', ''),
                data.get('dst_ip', ''),
                data.get('method', ''),
                data.get('host', ''),
                data.get('path', ''),
                data.get('user_agent', ''),
                data.get('channel', '')
            ])
    
    print(f"[+] Saved {len(http_data)} HTTP entries to {http_filename}")

def get_devices_count():
    with devices_lock:
        return len(devices)
