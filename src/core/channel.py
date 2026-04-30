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
    global current_channel, stop_hopping, static_mode, static_channel_value
    current_channel = 1
    stop_hopping = False
    static_mode = False
    static_channel_value = None

def set_static_mode(channel):
    global static_mode, static_channel_value, current_channel
    static_mode = True
    static_channel_value = channel
    current_channel = channel

def set_dinamic_mode(mode = "2.4G", user_channels):
        if mode == "custom" and len(channels) > 0:
            for item in user_channels:
                if item < 0 or item > 165:
                    print(f"[!] Channel {item} out of range")
                    return 0

            channels = user_channels
            return 1
        else if mode == "custom" and len(channels) = 0:
            print(f"[!] please add channel arr or switch mode")
            return 0
        else if mode == "2.4G":
            print("[ ] set standart channels for 2.4G")
            channels = [1,6,11]
            return 1
        else if mode == "5G":
            print("[ ] set standart channels for 5G")
            channels = [i for i in range(36, 49, 4)] + [i for i in range(52, 65, 4)] + [i for i in range(100, 145, 4)]
            return 1
        else:
            print("[!] somthing went wrong")
            return 0


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
    
    while not stop_hopping:
        for ch in channels:
            if stop_hopping: 
                break
            try:
                subprocess.run(["sudo", "iw", "dev", iface_mon, "set", "channel", str(ch)], 
                             capture_output=True, check=True)
                set_current_channel(ch)
                time.sleep(0.5)
            except:
                pass
