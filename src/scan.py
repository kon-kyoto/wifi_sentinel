import sys
import time
import signal
import threading
import subprocess

from scapy.all import sniff, RadioTap, Dot11
from scapy.layers.dhcp import DHCP

iface = None
iface_mon = None
write_prefix = None
stop_hopping = False
macs = []
channels = [i for i in range(1, 14)]

def chSwitch():
    while not stop_hopping:
        for ch in channels:
            if stop_hopping: break
            try:
                subprocess.run(["sudo", "iw", "dev", iface_mon, "set", "channel", str(ch)], 
                             capture_output=True, check=True)
                time.sleep(0.1)
            except:
                pass

def pktDHCPCheck(pkt):
    try:
        if pkt.haslayer(Dot11):
            mac = pkt.addr2
            if mac not in macs and mac != None:
                macs.append(mac)
                print(f"[+] New MAC: {mac}")    
    except:
        pass

def signalHandler(sig, frame):
    global stop_hopping
    print("\n[*] Stopping...")
    stop_hopping = True
    
    startStopMonitor(iface, iface_mon, "d")
    startStopNetwork("start")
    
    # Запись MAC адресов
    if write_prefix and macs:
        with open(f"{write_prefix}_macs.txt", "w") as f:
            for mac in macs:
                f.write(f"{mac}\n")
        print(f"[+] Saved {len(macs)} MACs to {write_prefix}_macs.txt")
    
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

def main():
    global iface, iface_mon, write_prefix, stop_hopping, macs     
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <interface> [-w prefix] [--wi time]")
        sys.exit(1)

    iface = sys.argv[1]
    iface_mon = iface + "mon"
    write_prefix = None
    write_interval = 30

    for i, arg in enumerate(sys.argv):
        if arg == "-w" and i+1 < len(sys.argv):
            write_prefix = sys.argv[i+1]
        elif arg == "--wi" and i+1 < len(sys.argv):
            write_interval = int(sys.argv[i+1]) 
    is_err = startStopMonitor(iface, iface_mon, "a") 
    if is_err: sys.exit(1)
    
    is_err = startStopNetwork("stop")
    if is_err: print("[!] Network stop failed, but continuing...")

    print(f"[*] Starting capture on {iface}")
    print(f"[ ] Writing PCAP to {write_prefix}.cap" if write_prefix else "[ ] Not writing to file")
    print(f"[ ] Write interval: {write_interval}s" if write_prefix else "")
    print(f"[ ] Press Ctrl+C to stop it\n")

    try:
        signal.signal(signal.SIGINT, signalHandler)
        hopper = threading.Thread(target=chSwitch, daemon=True)
        hopper.start()
        sniff(iface=iface_mon, prn=pktDHCPCheck, store=False)
    except Exception as e:
        print(f"[*] Error: {e}")
        stop_hopping = True
        signalHandler(None, None)

if __name__ == "__main__":
    main()
