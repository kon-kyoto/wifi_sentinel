"""
Command line interface argument parsing
"""
import sys
from argparse import ArgumentParser, Namespace

def parse_args() -> Namespace:
    parser = ArgumentParser(description="Wi-Fi Sentinel - Passive Airspace Monitor")
    parser.add_argument("iface", help="Wireless interface (e.g., wlan0)")
    parser.add_argument("-w", "--write", dest="write_prefix", help="Save output to CSV files")
    parser.add_argument("--http", action="store_true", dest="http_flag", help="HTTP traffic parsing only")
    parser.add_argument("--mac", action="store_true", dest="mac_flag", help="MAC address detection only")
    parser.add_argument("--prob", action="store_true", dest="prob_flag", help="Probe request/response detection only")
    parser.add_argument("-c", "--channel", dest="static_channel", type=int, choices=range(1, 14),
                       help="Use static channel (1-13) instead of hopping")
    parser.add_argument("-m", "--mode", dest="channel_mode", choices=["2.4G", "5G", "all", "custom"],
                       default="2.4G", help="Channel hopping mode (default: 2.4G)")
    parser.add_argument("--channels", dest="custom_channels", nargs="+", type=int,
                       help="Custom channel list for custom mode (e.g., --channels 1 6 11 36 40)")
    
    args = parser.parse_args()
    
    if args.channel_mode == "custom":
        if not args.custom_channels:
            print("[-] Error: --channels required when using custom mode")
            sys.exit(1)
        for ch in args.custom_channels:
            if ch < 1 or ch > 165:
                print(f"[-] Error: Channel {ch} out of range (1-165)")
                sys.exit(1)
    
    if args.static_channel:
        print(f"[*] Using static channel: {args.static_channel}")
    else:
        print(f"[*] Using dynamic channel mode: {args.channel_mode}")
        if args.channel_mode == "custom":
            print(f"[*] Custom channels: {args.custom_channels}")
    
    return args
