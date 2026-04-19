"""
Управление интерфейсом в режиме монитора.
Создает и удаляет интерфейсы в режиме монитора, управляет сетевыми сервисами.
"""
import subprocess
import time

def startStopMonitor(iface, iface_mon, mod):
    try:
        if mod == "a":
            print(f"[ ] Creating monitor interface {iface_mon}...")
            
            subprocess.run(["sudo", "ip", "link", "set", iface, "down"], 
                         capture_output=True, check=False)
            
            result = subprocess.run(["sudo", "iw", "dev", iface, "interface", "add", iface_mon, "type", "monitor"], 
                         capture_output=True, check=False)
            
            if result.returncode != 0:
                print(f"[-] Failed to create monitor interface")
                print(f"    Error: {result.stderr.decode()}")
                return 1
            
            subprocess.run(["sudo", "ip", "link", "set", iface_mon, "up"], 
                         capture_output=True, check=False)
            
            time.sleep(0.5)
            
            check = subprocess.run(["ip", "link", "show", iface_mon], 
                                 capture_output=True, text=True)
            
            if check.returncode == 0:
                print(f"[+] {iface_mon} is now in monitor mod")
                return 0
            else:
                print(f"[-] {iface_mon} not found after creation")
                return 1
                
        elif mod == "d":
            print(f"[ ] Removing monitor interface {iface_mon}...")
            
            subprocess.run(["sudo", "ip", "link", "set", iface_mon, "down"], 
                         capture_output=True, check=False)
            
            subprocess.run(["sudo", "iw", "dev", iface_mon, "del"], 
                         capture_output=True, check=False)
            
            time.sleep(0.5)
            
            subprocess.run(["sudo", "ip", "link", "set", iface, "up"], 
                         capture_output=True, check=False)
            
            print(f"[+] {iface} is now in managed mod")
            return 0
            
        return 0
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
                if "not-found" not in result.stderr:
                    print(f"[-] {mod} {net} failed (service may not exist)")
        return 0
    except Exception as e:
        print(f"[-] Something went wrong: {e}")
        return 1

