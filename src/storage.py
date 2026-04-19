"""
Device storage management.
Stores discovered devices and saves to CSV file.
"""
import csv
from threading import Lock

devices = {}
devices_lock = Lock()

def add_or_update_device(mac, channel, is_ap=False, ssid=""):
    with devices_lock:
        if mac not in devices:
            devices[mac] = {
                'essid': "",
                'channel': channel,
                'is_ap': False
            }
            print(f"[+] NEW DEVICE\tMAC: {mac}\tChannel: {channel}")
        
        if is_ap:
            devices[mac]['is_ap'] = True
        
        if ssid and ssid not in devices[mac]['essid']:
            if devices[mac]['essid']:
                devices[mac]['essid'] += f", {ssid}"
            else:
                devices[mac]['essid'] = ssid
            return True
        return False

def save_to_csv(write_prefix):
    if not write_prefix:
        return
    
    with devices_lock:
        if not devices:
            return
        filename = f"{write_prefix}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['mac', 'essid', 'channel', 'is_ap'])
            
            for mac, info in devices.items():
                writer.writerow([
                    mac,
                    info['essid'] if info['essid'] else "",
                    info['channel'],
                    "YES" if info['is_ap'] else "NO"
                ])
        
        print(f"\n[+] Saved {len(devices)} devices to {filename}")
        return filename

def get_devices_count():
    with devices_lock:
        return len(devices)
