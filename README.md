# 🛰️ CSI-Cipher v1.0
**Invisible Intrusion Detection via Wi-Fi Channel State Information (CSI) Analysis**

## 📝 Overview
CSI-Cipher is a privacy-preserving security module developed for the **DarkBot** ecosystem. Unlike traditional security systems that rely on cameras, CSI-Cipher utilizes the "radio shadows" cast by human bodies in a Wi-Fi field to detect movement and entry in real-time.

## 🛡️ Features
* **Device-Free Sensing:** Detects intruders without cameras, PIR sensors, or wearable devices.
* **Privacy-First:** No visual data is recorded; only radio wave amplitude fluctuations are analyzed.
* **DarkBot Integration:** Automated alerts and daily security summaries sent directly via WhatsApp.
* **Through-Wall Detection:** Leverages Wi-Fi's ability to propagate through physical obstacles to monitor hidden areas.

## ⚙️ How It Works
The system monitors **Channel State Information (CSI)**. Human bodies, being composed mostly of water, disrupt Wi-Fi signals through absorption and scattering. 

CSI-Cipher uses a **Statistical Spike Detection** algorithm:
1. **Baseline Extraction:** Establishes a "quiet room" signal profile.
2. **Signal-to-Noise Analysis:** Calculates the Standard Deviation ($\sigma$) of incoming subcarrier amplitudes.
3. **Threshold Triggering:** If $\Delta \sigma > Threshold$, a breach is logged and an alert is dispatched via Twilio/WhatsApp.

[Image of Wi-Fi CSI signal processing workflow from raw data to movement classification]

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy
* **Communication:** Twilio API (WhatsApp Gateway)
* **Simulation Hardware:** ESP32 CSI Tool Datasets (Figshare/Zenodo)

## 🚀 Future Roadmap
* **[ ]** Migration from CSV simulation to live ESP32 hardware.
* **[ ]** Implementation of a Kalman Filter for noise reduction.
* **[ ]** Multi-person counting using Machine Learning classification.
