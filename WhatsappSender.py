import pandas as pd
import os
import time
import serial
from dotenv import load_dotenv
from twilio.rest import Client
import datetime
import numpy as np

# Initialize
load_dotenv()

# Global Settings
SERIAL_PORT = 'COM5'
BAUD_RATE = 115200
BASELINE_FILE = "baseline.csv"
TRIPWIRE_THRESHOLD = 5.0  # Sensitivity: Adjust based on test results (e.g., 2.5 to 10.0)
COOLDOWN_SECONDS = 30     # Prevent alert spam
LAST_ALERT_TIME = 0

def load_baseline():
    """Loads the calibrated 'Quiet Room' profile from baseline.csv."""
    if not os.path.exists(BASELINE_FILE):
        print(f"❌ Error: {BASELINE_FILE} not found! Run 'python calibrate_csi.py' first.")
        return None
    try:
        df = pd.read_csv(BASELINE_FILE)
        return df
    except Exception as e:
        print(f"❌ Error reading baseline file: {e}")
        return None

def send_to_whatsapp(msg):
    global LAST_ALERT_TIME
    current_time = time.time()

    if current_time - LAST_ALERT_TIME < COOLDOWN_SECONDS:
        remaining = int(COOLDOWN_SECONDS - (current_time - LAST_ALERT_TIME))
        print(f"--- Cooldown active ({remaining}s remaining) ---")
        return

    try:
        account_sid = os.getenv('account_sid')
        auth_token = os.getenv('auth_token')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='whatsapp:+14155238886', 
            body=f'🚧 CSI-Tripwire: {msg}',
            to='whatsapp:+918219291979' 
        )
        
        LAST_ALERT_TIME = current_time
        print(f"✅ WhatsApp Alert Sent successfully!")
    except Exception as e:
        print(f"❌ WhatsApp Failed: {e}")

def monitor_tripwire():
    baseline = load_baseline()
    if baseline is None:
        return

    # Focus on stable subcarriers (10 to 50) to ignore noise at edges
    stable_indices = list(range(10, 50))
    b_mean = baseline.iloc[stable_indices]['mean_amplitude'].values
    b_std = baseline.iloc[stable_indices]['std_amplitude'].values

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        print(f"❌ Could not open serial port {SERIAL_PORT}: {e}")
        return

    print("--- CSI-Cipher: TRIPWIRE ARMED & MONITORING ---")
    print(f"Sensitivity Threshold: {TRIPWIRE_THRESHOLD}")

    while True:
        try:
            if ser.in_waiting > 0:
                line_raw = ser.readline()
                line = line_raw.decode('utf-8', errors='ignore').strip()
                
                if "CSI_DATA" in line and "[" in line:
                    try:
                        raw_numbers = line.split('[')[1].split(']')[0]
                        csi_values = np.array([int(x) for x in raw_numbers.split() if x.strip()])
                        
                        if len(csi_values) < 60: continue

                        # Calculate how much the current signal deviates from the baseline
                        current_amps = csi_values[stable_indices]
                        diff = np.abs(current_amps - b_mean)
                        
                        # Normalize the difference by the baseline standard deviation
                        z_scores = diff / (b_std + 0.1) # 0.1 to avoid division by zero
                        tripwire_score = np.mean(z_scores)

                        # Logic: High score means something just disturbed the Wi-Fi field
                        if tripwire_score > TRIPWIRE_THRESHOLD:
                            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            print(f"🚨 BEAM CROSSED! | Score: {tripwire_score:.2f} | Time: {timestamp}")
                            
                            # Log to local CSV
                            with open("tripwire_log.csv", "a") as f:
                                if os.stat("tripwire_log.csv").st_size == 0:
                                    f.write("Timestamp, Score\n")
                                f.write(f"{timestamp}, {tripwire_score:.2f}\n")
                            
                            send_to_whatsapp(f"Intruder detected crossing the beam at {timestamp} (Score: {tripwire_score:.2f})")
                        
                        # Optional: Print live score occasionally for tuning
                        # print(f"\rCurrent Tripwire Score: {tripwire_score:.2f}", end="")

                    except Exception as parse_error:
                        continue
        
        except Exception as e:
            print(f"❌ Serial Error: {e}")
            time.sleep(1)
            continue

if __name__ == "__main__":
    monitor_tripwire()
