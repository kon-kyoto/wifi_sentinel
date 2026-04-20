"""
Probe request/response storage
"""
import csv
import os
from threading import Lock

probe_data = []
probe_lock = Lock()

def add_probe_data(client_mac, target_mac, ssid, channel, probe_type):
    with probe_lock:
        probe_data.append({
            'client_mac': client_mac,
            'target_mac': target_mac,
            'ssid': ssid,
            'channel': channel,
            'type': probe_type
        })
    
    if probe_type == "request":
        if target_mac and target_mac != "FF:FF:FF:FF:FF:FF":
            print(f"\n[PROBE] {client_mac} -> {target_mac} (SSID: {ssid or 'broadcast'})")
        else:
            print(f"\n[PROBE] {client_mac} probing for: {ssid or 'any network'}")
    else:
        print(f"\n[PROBE RESP] {client_mac} <- {target_mac} (SSID: {ssid or 'unknown'})")

def get_probe_data():
    with probe_lock:
        return probe_data.copy()

def save_probe_to_csv(write_prefix, probe_data):
    if not write_prefix or not probe_data:
        return
    
    probe_filename = f"data/{write_prefix}_prob.csv"
    mode = 'a' if os.path.exists(probe_filename) else 'w'
    
    with open(probe_filename, mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if mode == 'w':
            writer.writerow(['client_mac', 'target_mac', 'ssid', 'channel', 'type'])
        
        for data in probe_data:
            writer.writerow([
                data.get('client_mac', ''),
                data.get('target_mac', ''),
                data.get('ssid', ''),
                data.get('channel', ''),
                data.get('type', '')
            ])
    
    print(f"[+] Saved {len(probe_data)} probe entries to {probe_filename}")
