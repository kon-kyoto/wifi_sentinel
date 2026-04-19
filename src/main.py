"""
Main entry point for Wi-Fi sniffer.
Initializes monitor interface, starts channel hopper and packet sniffer.
"""
import sys
import signal
import threading

from monitor import startStopMonitor, startStopNetwork
from channel import chSwitch, init_channel_state
from sniffer import start_sniffing, init_sniffer_state
from handler import signalHandler, out_prog, init_handler_state
from config import channels

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <interface> [-w prefix]")
        print(f"Example: {sys.argv[0]} wlan0 -w scan_output")
        sys.exit(1)

    iface = sys.argv[1]
    iface_mon = iface + "mon"
    write_prefix = None

    for i, arg in enumerate(sys.argv):
        if arg == "-w" and i+1 < len(sys.argv):
            write_prefix = sys.argv[i+1]
    
    init_handler_state(iface, iface_mon, write_prefix)
    init_channel_state()
    init_sniffer_state()
    
    is_err = startStopMonitor(iface, iface_mon, "a") 
    if is_err:
        out_prog("monitor mode")
        return
    
    is_err = startStopNetwork("stop")
    if is_err:
        print("[!] Network stop failed, but continuing...")

    print(f"\n[*] Starting capture on {iface}")
    print(f"[ ] Output CSV: {write_prefix}.csv" if write_prefix else "[ ] Not saving to file")
    print(f"[ ] Hopping channels: {channels[0]}-{channels[-1]}")
    print(f"[ ] Press Ctrl+C to stop it\n")

    try:
        signal.signal(signal.SIGINT, signalHandler)
        hopper = threading.Thread(target=chSwitch, args=(iface_mon,), daemon=True)
        hopper.start()
        start_sniffing(iface_mon)
    except Exception as e:
        out_prog(e)

if __name__ == "__main__":
    main()
