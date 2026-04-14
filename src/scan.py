import sys
import subprocess

from scapy.all import sniff

def startStopMonitor(iface, mod):
    try:
        subprocess.run(["ip", "link", "set", iface, "down"], check=True)
        subprocess.run(["iw", "dev", iface, "set", "type", mod], check=True)
        subprocess.run(["ip", "link", "set", iface, "up"], check=True)
        print(f"[+] {iface} is now in {mod} mod")
        
        return 0
    except:
        print("[-] somthing went wrong")
        if mod != "managed":
            is_err = startStopMonitor(iface, "managed")
            if is_err:
                print(f"!!!! Please check {iface} with command 'ip a'")
        return 1;

def pktHandler(pkt):
    pkt.summary()

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <interface> [-w prefix] [--wi time]")
        sys.exit(1)

    iface = sys.argv[1]
    write_prefix = None
    write_interval = 30

    for i, arg in enumerate(sys.argv):
        if arg == "-w" and i+1 < len(sys.argv):
            write_prefix = sys.argv[i+1]
        elif arg == "--wi" and i+1 < len(sys.argv):
            write_interval = sys.argv[i+1]

    is_err = startStopMonitor(iface, "monitor") 
    if is_err: sys.exit(1)

    print(f"[*] Startting capture on {iface}")
    print(f"[ ] Writing PCAP to {write_prefix}.cap" if write_prefix else "[ ] Not writing to file")
    print(f"[ ] Press Ctrl+C to stop it\n")

    try:
        sniff(iface=iface, prn=pktHandler, store=False)
    except KeyboardInterrupt:
        print("\n[*] Stopping...")
        startStopMonitor(iface, "managed")

        if write_prefix:
            pass

if __name__ == "__main__":
    main()
