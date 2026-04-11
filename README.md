# 📡 Wi-Fi Sentinel – Automated Airspace Monitoring System

> *"Know who's around you before they know you're watching."*

A modular, three‑stage offensive‑defensive Wi‑Fi security toolkit for penetration testers, blue teams, and home labs.

Built for Linux (Arch‑first), runs on a Raspberry Pi or any laptop with monitor‑mode support.

---

## 🧠 Philosophy

No cloud. No bloat. Just raw 802.11 frames and actionable intelligence.

Wi‑Fi Sentinel evolves in **three autonomous phases** – each one adds a new layer of awareness, analysis, and active response.

---

## 🗺️ Project Roadmap

### 🔰 Stage 1 – Silent Observer

**Passive device tracking without association.**

- Continuous airspace scanning in monitor mode  
- MAC‑based device fingerprinting (OUI vendor lookup)  
- SQLite database of known vs. unknown devices  
- Real‑time alerts for new/unrecognized MAC addresses  
- Lightweight Telegram / Slack webhook integration  

> *"You don't need to connect to see who's there."*

---

### 🕵️ Stage 2 – Traffic Profiler

**Metadata extraction and behavioral analysis.**

- Capture and parse probe requests + beacon frames  
- Build a live map of networks clients are searching for  
- Detect deauthentication / disassociation flood attacks  
- Signal strength (RSSI) trending over time  
- Export to KML for geographic visualization (Google Earth)  

> *"Every probe request tells a story."*

---

### ⚡ Stage 3 – Active Defender

**Automated counter‑measures against rogue infrastructure.**

- Identify Evil Twin / rogue APs by SSID + BSSID mismatch  
- Automatic deauthentication of malicious access points  
- Forensic packet capture of suspicious activity  
- Optional GPS tagging for physical device localization  
- Integration with alert dashboards (TheHive / MISP ready)  

> *"Don't just watch – respond."*

---

## 📦 What you'll build (without spoilers)

| Stage | Core skill | You'll learn |
|-------|------------|---------------|
| 1 | Python + Scapy | 802.11 frame parsing, event loops, SQLite |
| 2 | TShark / airodump‑ng | Probe analysis, attack detection, data visualization |
| 3 | Frame injection | Active defense, deauth attacks, forensic logging |

---

## 🧰 Hardware requirements (you provide)

- Wi‑Fi adapter with **monitor mode + frame injection** (e.g. Alfa AWUS036ACH)  
- Linux machine (Arch / Kali / Ubuntu)  
- (Optional) GPS dongle for wardriving mode

---

## 📁 Repository structure (planned)

```bash
wifi-sentinel/
├── stage1_observer/
│ ├── scanner.py
│ ├── db_handler.py
│ └── notifier.py
├── stage2_profiler/
│ ├── probe_sniffer.py
│ ├── attack_detector.py
│ └── visualizer.py
├── stage3_defender/
│ ├── rogue_hunter.py
│ ├── deauth_engine.py
│ └── forensics.py
├── config/
├── docs/
└── README.md
```

---

## 🚦 Current status

**Stage 1** – *design phase*  
Stage 2 – *planned*  
Stage 3 – *conceptual*

> Each stage will ship with its own `README.md`, example outputs, and a test harness.

---

## 🤝 Why open source?

Because Wi‑Fi security shouldn't be a black box.  
Learn the protocol. Defend your airspace. Build your own sentinel.

---

## 🧪 Tested on

- Arch Linux + Hyprland (my daily driver)  
- Raspberry Pi 4 (headless mode confirmed)  
- Alfa AWUS036ACH (Realtek RTL8812AU chipset)

---

## 📜 License

Do what you want – but don't use this to break laws you don't understand.

---

**Star this repo if you want to follow the journey.**  
PRs, ideas, and battle stories welcome.

— Your friendly neighborhood RF enthusiast 🐉
