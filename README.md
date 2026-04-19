# 📡 Wi-Fi Sentinel – Passive Airspace Monitor

> *"Know who's around you before they know you're watching."*

Wi‑Fi Sentinel is a **passive Wi‑Fi sniffer** that captures beacon frames, probe requests, probe responses, and HTTP traffic to discover devices, networks, and web activity in your vicinity — without ever associating with them.

Built for Linux (Arch, Kali, Raspberry Pi). Uses Scapy + monitor mode + channel hopping.

---

## ✨ Features

- ✅ Monitor mode interface management (`iw`)
- ✅ Multi‑channel hopping (channels 1–13) or static channel
- ✅ **MAC detection** – discover all nearby devices (APs + clients)
- ✅ **Probe tracking** – see which client is trying to connect to which AP or SSID
- ✅ **HTTP sniffing** – capture HTTP requests/responses (method, host, path, User-Agent)
- ✅ Real‑time console output with clear formatting
- ✅ CSV export (separate files for MAC, HTTP, and probe data)
- ✅ Graceful shutdown & network service restoration
- ✅ Thread‑safe channel tracking

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/yourusername/wifi-sentinel.git
cd wifi-sentinel
python3 -m venv venv
source venv/bin/activate
pip install scapy
```

### 2. Find your wireless interface

```bash
ip a
# Look for wlan0, wlp2s0, etc.
```

### 3. Run (requires sudo for monitor mode)

```bash
# Full mode (MAC + HTTP + PROBE) with CSV output
sudo python src/main.py wlan0 -w scan_results

# Only probe detection
sudo python src/main.py wlan0 --prob

# Only HTTP sniffing on static channel 6
sudo python src/main.py wlan0 --http -c 6

# MAC + PROBE without saving to file
sudo python src/main.py wlan0 --mac --prob
```

### 4. Stop with `Ctrl+C`

All data is saved to CSV files.

---

## 📊 Output Examples

### Console Output

```
[+] NEW	MAC: AA:BB:CC:DD:EE:FF	Channel: 6
    [AA:BB:CC:DD:EE:FF] Probing: HomeNetwork

[PROBE] 11:22:33:44:55:66 -> 77:88:99:AA:BB:CC (SSID: Starbucks)

[PROBE RESP] DD:EE:FF:00:11:22 <- AA:BB:CC:DD:EE:FF (SSID: MyWiFi)

[HTTP Request] GET example.com/index.html
    From: 192.168.1.100:54321
    User-Agent: Mozilla/5.0...
```

### CSV Files

**`scan_results_mac.csv`**
| mac | essid | channel | is_ap |
|-----|-------|---------|-------|
| AA:BB:CC:DD:EE:FF | HomeNetwork | 6 | NO |
| 11:22:33:44:55:66 | Starbucks, Airport | 11 | YES |

**`scan_results_http.csv`**
| src_ip | dst_ip | method | host | path | user_agent | channel |
|--------|--------|--------|------|------|------------|---------|
| 192.168.1.100 | 93.184.216.34 | GET | example.com | /index.html | Mozilla/5.0 | 6 |

**`scan_results_prob.csv`**
| client_mac | target_mac | ssid | channel | type |
|------------|------------|------|---------|------|
| 11:22:33:44:55:66 | FF:FF:FF:FF:FF:FF | HomeNetwork | 6 | request |
| 77:88:99:AA:BB:CC | AA:BB:CC:DD:EE:FF | Starbucks | 1 | response |

---

## 🧠 How It Works

```
main.py
  ├── monitor.py   → create wlan0mon, stop network managers
  ├── channel.py   → hop channels (1→13, 0.5 sec each) or static
  ├── sniffer.py   → capture Dot11 frames (scapy), dispatch to handlers
  ├── parser.py    → extract MAC, SSID, detect probe/beacon
  ├── http_parser.py → parse HTTP requests/responses
  ├── storage.py   → thread‑safe storage + CSV write + console output
  └── handler.py   → Ctrl+C cleanup, save all data
```

---

## 🛠️ Command Line Options

| Option | Description |
|--------|-------------|
| `<interface>` | Wireless interface (e.g., wlan0) |
| `-w <prefix>` | Save output to CSV files (`prefix_mac.csv`, `prefix_http.csv`, `prefix_prob.csv`) |
| `--http` | Enable HTTP traffic parsing only |
| `--mac` | Enable MAC address detection only |
| `--prob` | Enable probe request/response detection only |
| `-c <channel>` | Use static channel (1-13) instead of hopping |
| `-h, --help` | Show help message |

**Modes:**  
- No flags → Full functionality (MAC + HTTP + PROBE)  
- `--http` → HTTP only  
- `--mac` → MAC only  
- `--prob` → PROBE only  
- `--http --mac` → HTTP + MAC  
- `--mac --prob` → MAC + PROBE  
- `--http --prob` → HTTP + PROBE  

---

## 🛠️ Hardware Requirements

- Wi‑Fi adapter that supports **monitor mode**:
  - Alfa AWUS036ACH (RTL8812AU)
  - Atheros AR9271
  - Many internal Intel cards (`iw list` → "monitor")
- Linux OS (tested on Arch, Kali, Ubuntu, Raspberry Pi OS)

---

## 🗺️ Roadmap

| Stage | Status | Description |
|-------|--------|-------------|
| **1 – Observer** | ✅ Done | Passive discovery, MAC + PROBE + HTTP, CSV logging |
| **2 – Profiler** | 🔜 Planned | OUI vendor lookup, SQLite, RSSI trending, attack detection |
| **3 – Defender** | 🔜 Planned | Evil Twin detection, automated alerts, GPS tagging |

---

## 📁 Project Structure

```
wifi-sentinel/
├── src/
│   ├── main.py          # entry point, threading, CLI parsing
│   ├── config.py        # channels, write interval
│   ├── monitor.py       # start/stop monitor mode + network services
│   ├── channel.py       # channel hopping (threaded)
│   ├── sniffer.py       # scapy sniff loop, packet dispatch
│   ├── parser.py        # 802.11 frame parsing (MAC, SSID, probe/beacon)
│   ├── http_parser.py   # HTTP request/response parsing
│   ├── storage.py       # in‑memory storage + CSV write + console output
│   └── handler.py       # signal handling, cleanup
└── README.md
```

---

## 🧪 Tested On

- Arch Linux (6.12 kernel) + Alfa AWUS036ACH
- Raspberry Pi 4 (Raspberry Pi OS) + internal Wi‑Fi
- Kali Linux 2024 (virtualized)

---

## ⚠️ Legal & Ethics

- Only run this on **your own network** or with explicit permission.
- Passive sniffing is less intrusive than active attacks — but still check local laws.
- Don't be that person who deauths the coffee shop.

---

## 🤝 Contributing

PRs welcome for:
- OUI lookup (vendor by MAC prefix)
- SQLite instead of CSV
- Real‑time terminal UI (curses)
- RSSI collection and signal strength display

---

## 📄 License

MIT – do anything you want, but you assume all responsibility.

---

**Star if you use it. Fork if you improve it.**  
Questions? Open an issue.

— RF enthusiast
