"""
Monitor mode interface management.
Creates and removes monitor mode interfaces, controls network services.
"""
import subprocess

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
