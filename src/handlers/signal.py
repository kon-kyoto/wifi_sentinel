"""
Signal handling and cleanup
"""
import sys
import time
from src.core.monitor import startStopMonitor, startStopNetwork
from src.core.channel import stop_channel_hopping
from src.core.sniffer import get_packet_count, get_http_data
from src.storage.devices import save_to_csv, get_devices_count
from src.storage.http_store import save_http_to_csv
from src.storage.probe_store import save_probe_to_csv, get_probe_data

iface = None
iface_mon = None
write_prefix = None

def init_handler_state(i, i_mon, prefix):
    global iface, iface_mon, write_prefix
    iface = i
    iface_mon = i_mon
    write_prefix = prefix

def signalHandler(sig, frame):
    print("\n[*] Stopping...")
    print(f"[*] Statistics:")
    print(f"    Total packets captured: {get_packet_count()}")
    
    stop_channel_hopping()
    time.sleep(0.5)
    
    startStopMonitor(iface, iface_mon, "d")
    startStopNetwork("start")
    
    if write_prefix:
        save_to_csv(write_prefix)
        http_data = get_http_data()
        if http_data:
            save_http_to_csv(write_prefix, http_data)
        probe_data = get_probe_data()
        if probe_data:
            save_probe_to_csv(write_prefix, probe_data)
        print(f"[*] Total devices: {get_devices_count()}")
    
    sys.exit(0)

def out_prog(e):
    print(f"[*] Error: {e}")
    stop_channel_hopping()
    signalHandler(None, None)
