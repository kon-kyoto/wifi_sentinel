#!/usr/bin/env python3
"""
Wi-Fi Sentinel - Passive Airspace Monitor
"""
import sys
import signal

from src.cli import parse_args
from src.core.monitor import startStopMonitor, startStopNetwork
from src.core.channel import chSwitch, init_channel_state, set_static_mode
from src.core.sniffer import start_sniffing, init_sniffer_state, set_http_enabled, set_mac_enabled, set_prob_enabled
from src.handlers.signal import signalHandler, out_prog, init_handler_state
from src.storage.devices import load_existing_devices

def main():
    args = parse_args()

    init_handler_state(args.iface, args.iface + "mon", args.write_prefix)
    init_channel_state()
    init_sniffer_state()
    
    if args.http_flag or args.mac_flag or args.prob_flag:
        set_http_enabled(args.http_flag)
        set_mac_enabled(args.mac_flag)
        set_prob_enabled(args.prob_flag)
    else:
        set_mac_enabled(True)
        set_prob_enabled(True)
    
    if args.static_channel:
        set_static_mode(args.static_channel)
    
    if startStopMonitor(args.iface, args.iface + "mon", "a"):
        out_prog("monitor mode")
        return
    
    startStopNetwork("stop")
    
    print(f"\n[*] Starting capture on {args.iface}")
    
    if args.write_prefix:
        if args.http_flag or (not args.http_flag and not args.mac_flag and not args.prob_flag):
            print(f"[ ] HTTP output: {args.write_prefix}_http.csv")
        if args.mac_flag or (not args.http_flag and not args.mac_flag and not args.prob_flag):
            print(f"[ ] MAC output: {args.write_prefix}_mac.csv")
        if args.prob_flag or (not args.http_flag and not args.mac_flag and not args.prob_flag):
            print(f"[ ] PROB output: {args.write_prefix}_prob.csv")
        load_existing_devices(args.write_prefix)
    
    if args.static_channel:
        print(f"[ ] Channel: static {args.static_channel}")
    else:
        from src.config import channels
        print(f"[ ] Hopping channels: {channels[0]}-{channels[-1]}")
    
    print(f"[ ] Press Ctrl+C to stop it\n")
    
    signal.signal(signal.SIGINT, signalHandler)
    
    if not args.static_channel:
        import threading
        hopper = threading.Thread(target=chSwitch, args=(args.iface + "mon",), daemon=True)
        hopper.start()
    
    start_sniffing(args.iface + "mon")

if __name__ == "__main__":
    main()
