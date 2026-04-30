"""
Channel hopping management
"""
import subprocess
import time
from threading import Lock
from src.config import channels

current_channel = 1
stop_hopping = False
channel_lock = Lock()
static_mode = False
static_channel_value = None

def init_channel_state():
    global current_channel, stop_hopping, static_mode, static_channel_value, channels
    current_channel = 1
    stop_hopping = False
    static_mode = False
    static_channel_value = None
    channels = []

def set_static_mode(channel):
    global static_mode, static_channel_value, current_channel
    static_mode = True
    static_channel_value = channel
    current_channel = channel

def set_dynamic_mode(mode="2.4G", user_channels=None):
    global channels
    
    if mode == "custom":
        if user_channels and len(user_channels) > 0:
            # Validate channel range
            for item in user_channels:
                if item < 1 or item > 165:
                    print(f"[!] Channel {item} out of range (1-165)")
                    return False
            
            channels = user_channels.copy()
            print(f"[+] Custom channel set: {channels}")
            return True
        else:
            print(f"[!] Please provide channel list for custom mode")
            return False
            
    elif mode == "2.4G":
        print("[ ] Setting standard channels for 2.4 GHz band")
        channels = [1, 6, 11]
        print(f"[+] 2.4 GHz channels: {channels}")
        return True
        
    elif mode == "5G":
        print("[ ] Setting standard channels for 5 GHz band")
        channels = [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144]
        print(f"[+] 5 GHz channels: {channels}")
        return True
        
    elif mode == "all":
        print("[ ] Setting all available channels")
        channels = list(range(1, 14)) + [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165]
        print(f"[+] All channels: {channels}")
        return True
        
    else:
        print(f"[!] Unknown mode: {mode}. Available: 2.4G, 5G, all, custom")
        return False

def get_current_channel():
    with channel_lock:
        return current_channel

def set_current_channel(ch):
    with channel_lock:
        global current_channel
        current_channel = ch

def stop_channel_hopping():
    global stop_hopping
    stop_hopping = True

def chSwitch(iface_mon):
    global stop_hopping
    
    if static_mode and static_channel_value:
        try:
            subprocess.run(["sudo", "iw", "dev", iface_mon, "set", "channel", str(static_channel_value)], 
                         capture_output=True, check=True)
            set_current_channel(static_channel_value)
            print(f"[+] Set static channel to {static_channel_value}")
        except Exception as e:
            print(f"[-] Failed to set static channel: {e}")
        while not stop_hopping:
            time.sleep(1)
        return

    if not channels:
        print("[!] No channels configured, using default 2.4GHz channels")
        set_dynamic_mode("2.4G")
    
    print(f"[*] Starting channel hopping on {len(channels)} channels: {channels}")
    
    while not stop_hopping:
        for ch in channels:
            if stop_hopping: 
                break
            try:
                subprocess.run(["sudo", "iw", "dev", iface_mon, "set", "channel", str(ch)], 
                             capture_output=True, check=True)
                set_current_channel(ch)
                time.sleep(0.3)
            except subprocess.CalledProcessError as e:
                print(f"[-] Failed to set channel {ch}: {e}")
                time.sleep(0.1)
            except Exception as e:
                print(f"[-] Unexpected error on channel {ch}: {e}")
                time.sleep(0.1)
