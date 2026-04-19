# 📡 Wi-Fi Sentinel – Passive Airspace Monitor

> *"Know who's around you before they know you're watching."*

Wi‑Fi Sentinel is a **passive Wi‑Fi sniffer** that captures beacon frames and probe requests to discover devices and networks in your vicinity — without ever associating with them.

Built for Linux (Arch, Kali, Raspberry Pi). Uses Scapy + monitor mode + channel hopping.

---

## ✨ Current Features (Stage 1 – Complete)

- ✅ Monitor mode interface management (`iw`)
- ✅ Multi‑channel hopping (channels 1–13)
- ✅ Real‑time device discovery:
  - Access Points (beacon frames) → SSID + channel
  - Client devices (probe requests) → which networks they are looking for
- ✅ CSV export with MAC, ESSID, channel, AP/client flag
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
pip install -r requirements.txt
```

### 2. Find your wireless interface

```bash
ip a
# Look for wlan0, wlp2s0, etc.
```

### 3. Run (requires sudo for monitor mode)

```bash
sudo python src/main.py wlan0 -w scan_results
```

### 4. Stop with `Ctrl+C`

All discovered devices are saved to `scan_results.csv`.

---

## 📊 Output Example (CSV)

| mac               | essid                          | channel | is_ap |
|-------------------|--------------------------------|---------|-------|
| AA:BB:CC:DD:EE:FF | MyHomeNetwork                  | 6       | YES   |
| 11:22:33:44:55:66 | Starbucks Wi-Fi, Xfinity       | 11      | NO    |
| DE:AD:BE:EF:00:01 | (empty)                        | 1       | NO    |

> A device with `is_ap = NO` and an `essid` is a **client probing** for known networks.  
> Multiple SSIDs in one row = same MAC probing for several networks.

---

## 🧠 How It Works

```
main.py
  ├── monitor.py   → create wlan0mon, stop network managers
  ├── channel.py   → hop channels (1→13, 0.5 sec each)
  ├── sniffer.py   → capture Dot11 frames (scapy)
  ├── parser.py    → extract MAC, SSID, probe/beacon
  ├── storage.py   → thread‑safe device dictionary + CSV write
  └── handler.py   → Ctrl+C cleanup, save data
```

---

## 🛠️ Hardware Requirements

- Wi‑Fi adapter that supports **monitor mode**:
  - Alfa AWUS036ACH (RTL8812AU)
  - Atheros AR9271
  - Many internal Intel cards (`iw list` → "monitor")
- Linux OS (tested on Arch, Kali, Ubuntu, Raspberry Pi OS)

---

## 🗺️ Roadmap (what's next)

| Stage | Status | Description |
|-------|--------|-------------|
| **1 – Observer** | ✅ Done | Passive discovery, CSV logging |
| **2 – Profiler** | 🔜 Planned | OUI vendor lookup, SQLite, RSSI trending, attack detection (deauth floods) |
| **3 – Defender** | 🔜 Planned | Evil Twin detection, automated deauth of rogue APs, GPS tagging |

---

## 📁 Project Structure

```
wifi-sentinel/
├── src/
│   ├── main.py          # entry point, threading
│   ├── config.py        # channels, write interval
│   ├── monitor.py       # start/stop monitor mode + network services
│   ├── channel.py       # channel hopping (threaded)
│   ├── sniffer.py       # scapy sniff loop
│   ├── parser.py        # 802.11 frame parsing
│   ├── storage.py       # in‑memory device store + CSV
│   └── handler.py       # signal handling, cleanup
├── requirements.txt     # scapy only
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
- RSSI collection

---

## 📄 License

MIT – do anything you want, but you assume all responsibility.

---

**Star if you use it. Fork if you improve it.**  
Questions? Open an issue.

— RF enthusiast

Теперь README не расходится с кодом. Пользователь, прочитав его, сразу поймет, что запускать `sudo python src/main.py wlan0 -w out`, и получит ровно то, что обещано.
