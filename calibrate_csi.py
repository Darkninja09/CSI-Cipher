import pandas as pd
import numpy as np
import serial
import time
import os

# Configuration
SERIAL_PORT = 'COM5'
BAUD_RATE = 115200
CALIBRATION_DURATION = 30  # Seconds to record the empty room
BASELINE_FILE = "baseline.csv"

def calibrate():
    print(f"--- CSI-Cipher: CALIBRATION MODE ---")
    print(f"Please ensure the room is EMPTY for the next {CALIBRATION_DURATION} seconds.")
    print(f"Connecting to {SERIAL_PORT}...")

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        print(f"❌ Error: Could not open serial port: {e}")
        return

    raw_data = []
    start_time = time.time()
    
    print("⏳ Recording baseline... Stay out of the Wi-Fi field!")
    
    while time.time() - start_time < CALIBRATION_DURATION:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if "CSI_DATA" in line and "[" in line:
                    raw_numbers = line.split('[')[1].split(']')[0]
                    csi_values = [int(x) for x in raw_numbers.split() if x.strip()]
                    
                    if len(csi_values) > 20:
                        raw_data.append(csi_values)
                        
                        # Progress indicator
                        elapsed = int(time.time() - start_time)
                        percent = int((elapsed / CALIBRATION_DURATION) * 100)
                        print(f"\rProgress: [{'#' * (percent // 5)}{'.' * (20 - percent // 5)}] {percent}%", end="")
        except Exception as e:
            continue

    ser.close()
    print("\n\n✅ Data Collection Complete.")

    if len(raw_data) < 10:
        print("❌ Error: Not enough data collected. Check your ESP32 output.")
        return

    # Process baseline
    df = pd.DataFrame(raw_data)
    
    # Calculate Mean and StdDev for each subcarrier
    baseline = pd.DataFrame({
        'subcarrier': range(len(df.columns)),
        'mean_amplitude': df.mean(),
        'std_amplitude': df.std()
    })

    baseline.to_csv(BASELINE_FILE, index=False)
    print(f"💾 Baseline fingerprint saved to {BASELINE_FILE}")
    print("This file now represents your 'Quiet Room'. Any deviation from this will be human movement.")

if __name__ == "__main__":
    calibrate()
