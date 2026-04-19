"""
Signal handling and cleanup.
Manages graceful shutdown, network restoration and data saving.
"""
import sys
import time
from monitor import startStopMonitor, startStopNetwork
from storage import save_to_csv, get_devices_count
from channel import stop_channel_hopping

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
    stop_channel_hopping()
    
    time.sleep(0.5)
    
    startStopMonitor(iface, iface_mon, "d")
    startStopNetwork("start")
    
    if write_prefix:
        save_to_csv(write_prefix)
        print(f"[*] Total devices: {get_devices_count()}")
    
    sys.exit(0)

def out_prog(e):
    print(f"[*] Error: {e}")
    stop_channel_hopping()
    signalHandler(None, None)
