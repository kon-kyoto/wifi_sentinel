"""
Главная точка входа для Wi-Fi сниффера.
Инициализирует монитор режим, запускает переключатель каналов и сниффер пакетов.
"""
import sys
import signal
import threading

from monitor import startStopMonitor, startStopNetwork
from channel import chSwitch, init_channel_state, set_static_mode
from sniffer import start_sniffing, init_sniffer_state, set_http_enabled, set_mac_enabled, set_prob_enabled
from handler import signalHandler, out_prog, init_handler_state
from storage import load_existing_devices
from config import channels, static_channel

def print_usage():
    print(f"Usage: {sys.argv[0]} <interface> [options]")
    print(f"Options:")
    print(f"  -w <prefix>     Save output to CSV files ({prefix}_mac.csv and {prefix}_http.csv)")
    print(f"  --http          Enable HTTP traffic parsing only")
    print(f"  --mac           Enable MAC address detection only")
    print(f"  --prob          Enable probe request/response detection only")
    print(f"  -c <channel>    Use static channel (1-13) instead of hopping")
    print(f"  -h, --help      Show this help message")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print_usage()
        sys.exit(0 if len(sys.argv) > 1 else 1)

    iface = sys.argv[1]
    iface_mon = iface + "mon"
    write_prefix = None
    http_flag = False
    mac_flag = False
    prob_flag = False
    global static_channel
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "-w" and i+1 < len(sys.argv):
            write_prefix = sys.argv[i+1]
            i += 2
        elif arg == "--http":
            http_flag = True
            i += 1
        elif arg == "--mac":
            mac_flag = True
            i += 1
        elif arg == "--prob":
            prob_flag = True
            i += 1
        elif arg == "-c" and i+1 < len(sys.argv):
            try:
                static_channel = int(sys.argv[i+1])
                if static_channel < 1 or static_channel > 13:
                    print(f"[-] Channel must be between 1 and 13")
                    sys.exit(1)
                print(f"[*] Using static channel: {static_channel}")
                i += 2
            except ValueError:
                print(f"[-] Invalid channel number: {sys.argv[i+1]}")
                sys.exit(1)
        else:
            print(f"[-] Unknown option: {arg}")
            print_usage()
            sys.exit(1)
    
    init_handler_state(iface, iface_mon, write_prefix)
    init_channel_state()
    init_sniffer_state()
    
    if static_channel:
        set_static_mode(static_channel)
    
    is_err = startStopMonitor(iface, iface_mon, "a") 
    if is_err:
        out_prog("monitor mode")
        return
    
    is_err = startStopNetwork("stop")
    if is_err:
        print("[!] Network stop failed, but continuing...")

    print(f"\n[*] Starting capture on {iface}")
    
    if write_prefix:
        if http_flag or (not http_flag and not mac_flag and not prob_flag):
            print(f"[ ] HTTP output: {write_prefix}_http.csv")
        if mac_flag or (not http_flag and not mac_flag and not prob_flag):
            print(f"[ ] MAC output: {write_prefix}_mac.csv")
        if prob_flag:
            print(f"[ ] PROB output: {write_prefix}_prob.csv")
        load_existing_devices(write_prefix)
    else:
        print(f"[ ] Not saving to file")
    
    if static_channel:
        print(f"[ ] Channel: static {static_channel} (no hopping)")
    else:
        print(f"[ ] Hopping channels: {channels[0]}-{channels[-1]}")
    
    if http_flag or (not http_flag and not mac_flag and not prob_flag):
        print(f"[ ] HTTP parsing: ENABLED")
        set_http_enabled(True)
    else:
        set_http_enabled(False)
        print(f"[ ] HTTP parsing: DISABLED")
    
    if mac_flag or (not http_flag and not mac_flag and not prob_flag):
        print(f"[ ] MAC detection: ENABLED")
        set_mac_enabled(True)
    else:
        set_mac_enabled(False)
        print(f"[ ] MAC detection: DISABLED")
    
    if prob_flag or (not http_flag and not mac_flag and not prob_flag):
        print(f"[ ] PROBE detection: ENABLED")
        set_prob_enabled(True)
    else:
        set_prob_enabled(False)
        print(f"[ ] PROBE detection: DISABLED")
    
    print(f"[ ] Press Ctrl+C to stop it\n")

    try:
        signal.signal(signal.SIGINT, signalHandler)
        
        if not static_channel:
            hopper = threading.Thread(target=chSwitch, args=(iface_mon,), daemon=True)
            hopper.start()
        
        start_sniffing(iface_mon)
    except Exception as e:
        out_prog(e)

if __name__ == "__main__":
    main()
