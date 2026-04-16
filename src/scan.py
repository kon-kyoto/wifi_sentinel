import sys
import signal
import subprocess

from scapy.all import sniff

iface = None
iface_mon = None
write_prefix = None

# Create class for signal and iface in future pls

def signalHandler(sig, frame):
    print("\n[*] Stopping...")
    startStopMonitor(iface, iface_mon, "d")
    startStopNetwork("start")

    if write_prefix:
        pass

def startStopMonitor(iface, iface_mon, mod):
    try:
        if mod == "a":
            subprocess.run(["sudo", "ip", "link", "set", iface, "down"], check=True)
            subprocess.run(["sudo", "iw", "dev", iface,  "interface", "add", iface_mon, "type", "monitor"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", iface_mon, "up"])
            print(f"[+] {iface_mon} is now in monitor mod")
        elif mod == "d":
            subprocess.run(["sudo", "ip", "link", "set", iface_mon, "down"], check=True)
            subprocess.run(["sudo", "iw", "dev", iface_mon, "del"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", iface, "up"], check=True)
            print(f"[+] {iface} is now in managed mod")
        
        return 0
    except:
        print("[-] somthing went wrong")
        print(f"!!!! Please check {iface} with command 'ip a'")
        return 1;

def startStopNetwork(mod):
    print(f"[ ] {mod} network process")
    try:
        net_list = ["wpa_supplicant", "iwd", "NetworkManager"]
        for net in net_list:
            subprocess.run(["sudo", "systemctl", mod, net])
            print(f"[ ] {mod} {net}")
        print(f"[+] {mod} network success")

        return 0
    except:
        print("[-] somthing went wrong")
        
        return 1

def pktHandler(pkt):
    pkt.show()

def main():
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
            write_interval = sys.argv[i+1]

    is_err = startStopMonitor(iface, iface_mon, "a") 
    is_err = startStopNetwork("stop")
    if is_err: sys.exit(1)

    print(f"[*] Startting capture on {iface}")
    print(f"[ ] Writing PCAP to {write_prefix}.cap" if write_prefix else "[ ] Not writing to file")
    print(f"[ ] Press Ctrl+C to stop it\n")

    signal.signal(signal.SIGINT, signalHandler)

    try:
        sniff(iface=iface_mon, prn=pktHandler)
    except Exception as e:
        print(f"[*] Error: {e}")
        signalHandler(None, None)

if __name__ == "__main__":
    main()
