# 📡 Wi-Fi Sentinel – Your Digital Motion Detector

> *"Silence in the air is also a signal. But mostly, it's just noise."*

Imagine this: you're sitting in a coffee shop, sipping your latte, while dozens of devices around you are screaming into the void: "Where's my home network? What about Starbucks? And that Wi-Fi I saved three years ago?"

Wi‑Fi Sentinel listens to this **quiet scream**.
It doesn't connect. It doesn't blink. It doesn't make a sound. It just **knows** who's around.

---

## ✨ What This Beast Can Do

| Mode | What it sees | Why it matters |
|------|--------------|----------------|
| **MAC detection** | Every device in range | "Who's walking around here?" |
| **PROBE tracking** | Client → which network they want | "You're looking for Starbucks? Got it, noted." |
| **HTTP sniffing** | Sites, headers, POST data | "Oh, someone's visiting... (no judgment, it's for science)" |
| **Channel hopping** | Jumps across 13 channels | "I won't miss a thing. I'm everywhere." |

> *"A passive scanner leaves no traces. Like a ghost keeping a diary."*

---

## 🚀 One‑Line Launch

```bash
# Clone it
git clone https://github.com/yourusername/wifi-sentinel.git
cd wifi-sentinel

# Set up your environment
python3 -m venv venv
source venv/bin/activate
pip install scapy

# Poof — you're in the matrix
sudo python sentinel.py wlan0 -w my_scan
```

Stop with `Ctrl+C`. Everything saves to CSV.

---

## 🎮 Modes for Every Mood

```bash
# Full throttle (MAC + PROBE + HTTP)
sudo python sentinel.py wlan0 -w full_scan

# Just peeking at HTTP traffic
sudo python sentinel.py wlan0 --http

# Who's knocking on whose door (probe requests/responses)
sudo python sentinel.py wlan0 --prob

# Sniper mode — sit on one channel
sudo python sentinel.py wlan0 -c 6

# Everything, everywhere, all at once
sudo python sentinel.py wlan0 --mac --prob --http -w everything
```

> *"Flags are like mantras. Learn them, become a sniffing jedi."*

---

## 📂 What You Get

### `scan_mac.csv` — Who's who
| mac | essid | channel | is_ap |
|-----|-------|---------|-------|
| AA:BB:CC:DD:EE:FF | HomeNetwork | 6 | YES |
| 11:22:33:44:55:66 | Starbucks, Airport | 1 | NO |

### `scan_prob.csv` — Who's knocking on whom
| client_mac | target_mac | ssid | type |
|------------|------------|------|-------|
| AA:BB:CC:DD:EE:FF | FF:FF:FF:FF:FF:FF | HomeNetwork | request |
| 11:22:33:44:55:66 | 77:88:99:AA:BB:CC | CoffeeShop | response |

### `scan_http.csv` — What they're browsing
| timestamp | src_ip | host | path | user_agent | post_data |
|-----------|--------|------|------|------------|-----------|
| 2025-01-15 14:23:05 | 192.168.1.100 | example.com | /login | Mozilla/5.0 | user=admin&pass=*** |

> *"CSV is a device's confession. They just don't know they're being read."*

---

## 🧠 How It Works (for the curious)

```
Your Wi-Fi adapter (monitor mode)
         ↓
   hops across channels (1-13)
         ↓
   captures everything (scapy)
         ↓
   ┌─────────────┼─────────────┐
   ↓             ↓             ↓
  MAC          PROBE         HTTP
(beacon/    (request/     (request/
 probe req)   response)     response)
   ↓             ↓             ↓
  CSV          CSV           CSV
```

**You don't connect → They don't see you.**  
**You listen → You know.**

> *"The best way to stay invisible is not to glow. Sentinel doesn't glow."*

---

## 🛠️ Hardware You'll Need

- **Wi-Fi adapter with monitor mode support**
  - Alfa AWUS036ACH (the people's champ)
  - Atheros AR9271 (old but gold)
  - Some internal Intel cards (check with `iw list | grep monitor`)

- **Linux** (Arch, Kali, Ubuntu, Raspberry Pi OS — take your pick)

> *"Windows won't cut it. Seriously. Don't even try."*

---

## 🧪 Tested On

- ✅ Arch Linux + Alfa AWUS036ACH (kernel 6.12)
- ✅ Raspberry Pi 4 + built‑in Wi‑Fi
- ✅ Kali Linux (virtualized — yes, it works too)

---

## ⚠️ Legal Mantra

- This tool is for **your own networks** or with **written permission**.
- Passive sniffing isn't hacking, but laws can be weird.
- Don't be that person who deauths the coffee shop.

> *"With great power comes great responsibility. And a little bit of paranoia."*

---

## 🤻 Want to Contribute?

Pull requests are welcome with open arms:

- OUI lookup (identify vendors by MAC prefix)
- Replace CSV with SQLite
- Beautiful TUI (curses) with real‑time updates
- RSSI signal strength display

---

## 📄 License

**MIT** — do whatever you want, but you own the consequences.

> *"Fork if you improve it. Star if you use it. Open an issue if it breaks."*

---

**Questions?** Open an issue.  
**Ideas?** Spill them.  
**Creeped out?** That's healthy.

— Your friend who listens to the airwaves 👻
