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
    
    args = parser.parse_args()
    
    if args.static_channel:
        print(f"[*] Using static channel: {args.static_channel}")
    
    return args
