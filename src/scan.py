import sys
import time
import signal
import threading
import subprocess
import csv

from scapy.all import sniff, Dot11, Dot11ProbeReq, Dot11Beacon, Dot11Elt

iface = None
iface_mon = None
write_prefix = None
stop_hopping = False
channels = [i for i in range(1, 14)]
current_channel = 1

# mac -> {essid, channel, is_ap}
devices = {}

def extract_ssid(pkt):
    """Извлечение SSID из пакета"""
    try:
        elt = pkt.getlayer(Dot11Elt)
        while elt:
            if elt.ID == 0:
                return elt.info.decode('utf-8', errors='ignore')
            elt = elt.payload.getlayer(Dot11Elt)
    except:
        pass
    return ""

def chSwitch():
    global current_channel
    while not stop_hopping:
        for ch in channels:
            if stop_hopping: 
                break
            try:
                subprocess.run(["sudo", "iw", "dev", iface_mon, "set", "channel", str(ch)], 
                             capture_output=True, check=True)
                current_channel = ch
                time.sleep(0.1)
            except:
                pass

def pktHandler(pkt):
    global devices
    
    try:
        if not pkt.haslayer(Dot11):
            return
        
        mac = pkt.addr2 or pkt.addr3
        if not mac:
            return
        
        mac = str(mac).upper()
        
        if mac not in devices:
            devices[mac] = {
                'essid': "",
                'channel': current_channel,
                'is_ap': False
            }
            print(f"\n[+] NEW DEVICE")
            print(f"    MAC: {mac}")
            print(f"    Channel: {current_channel}")
        
        if pkt.haslayer(Dot11ProbeReq):
            ssid = extract_ssid(pkt)
            if ssid and ssid not in devices[mac]['essid']:
                if devices[mac]['essid']:
                    devices[mac]['essid'] += f", {ssid}"
                else:
                    devices[mac]['essid'] = ssid
                print(f"    [{mac}] Probing: {ssid}")
        
        elif pkt.haslayer(Dot11Beacon):
            ssid = extract_ssid(pkt)
            if ssid and ssid != "":
                devices[mac]['is_ap'] = True
                if ssid not in devices[mac]['essid']:
                    if devices[mac]['essid']:
                        devices[mac]['essid'] += f", {ssid}"
                    else:
                        devices[mac]['essid'] = ssid
                devices[mac]['channel'] = current_channel
                
    except Exception as e:
        pass

def save_to_csv():
    if not write_prefix or not devices:
        return
    
    filename = f"{write_prefix}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['mac', 'essid', 'channel', 'is_ap'])
        
        for mac, info in devices.items():
            writer.writerow([
                mac,
                info['essid'] if info['essid'] else "",
                info['channel'],
                "YES" if info['is_ap'] else "NO"
            ])
    
    print(f"\n[+] Saved {len(devices)} devices to {filename}")

def signalHandler(sig, frame):
    global stop_hopping
    print("\n[*] Stopping...")
    stop_hopping = True
    
    time.sleep(0.5)
    
    startStopMonitor(iface, iface_mon, "d")
    startStopNetwork("start")
    
    if write_prefix:
        save_to_csv()
    
    sys.exit(0)

def startStopMonitor(iface, iface_mon, mod):
    try:
        if mod == "a":
            subprocess.run(["sudo", "ip", "link", "set", iface, "down"], capture_output=True, check=True)
            subprocess.run(["sudo", "iw", "dev", iface, "interface", "add", iface_mon, "type", "monitor"], 
                         capture_output=True, check=True)
            subprocess.run(["sudo", "ip", "link", "set", iface_mon, "up"], capture_output=True, check=True)
            print(f"[+] {iface_mon} is now in monitor mod")
        elif mod == "d":
            subprocess.run(["sudo", "ip", "link", "set", iface_mon, "down"], capture_output=True, check=True)
            subprocess.run(["sudo", "iw", "dev", iface_mon, "del"], capture_output=True, check=True)
            subprocess.run(["sudo", "ip", "link", "set", iface, "up"], capture_output=True, check=True)
            print(f"[+] {iface} is now in managed mod")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"[-] Command failed: {e}")
        print(f"!!!! Please check {iface} with command 'ip a'")
        return 1
    except Exception as e:
        print(f"[-] Something went wrong: {e}")
        return 1

def startStopNetwork(mod):
    print(f"[ ] {mod} network process")
    try:
        net_list = ["wpa_supplicant", "iwd", "NetworkManager"]
        for net in net_list:
            result = subprocess.run(["sudo", "systemctl", mod, net], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[+] {mod} {net}")
            else:
                print(f"[-] {mod} {net} failed (service may not exist)")
        return 0
    except Exception as e:
        print(f"[-] Something went wrong: {e}")
        return 1

def out_prog(e):
    print(f"[*] Error: {e}")
    global stop_hopping
    stop_hopping = True
    signalHandler(None, None)

def main():
    global iface, iface_mon, write_prefix, stop_hopping
    
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
        hopper = threading.Thread(target=chSwitch, daemon=True)
        hopper.start()
        sniff(iface=iface_mon, prn=pktHandler, store=False)
    except Exception as e:
        out_prog(e)

if __name__ == "__main__":
    main()
