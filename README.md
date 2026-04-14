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

```bash
# Создание venv
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt

# Сохранение зависимостей
pip freeze > requirements.txt
```
