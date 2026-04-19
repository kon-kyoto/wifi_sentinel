"""
Channel hopping controller.
Cycles through configured channels with thread-safe state management.
"""
import subprocess
import time
from threading import Lock
from config import channels

current_channel = 1
stop_hopping = False
channel_lock = Lock()

def init_channel_state():
    global current_channel, stop_hopping
    current_channel = 1
    stop_hopping = False

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
