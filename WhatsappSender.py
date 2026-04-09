import pandas as pd
import os
import time
import serial
from dotenv import load_dotenv
from twilio.rest import Client

# Initialize
load_dotenv()
ser = serial.Serial('COM5', 115200, timeout=1)

# Global Settings
COOLDOWN_SECONDS = 10  # 5 Minutes
LAST_ALERT_TIME = 0

def send_to_whatsapp(msg):
    global LAST_ALERT_TIME
    current_time = time.time()

    # Check if we are still in the cooldown period
    if current_time - LAST_ALERT_TIME < COOLDOWN_SECONDS:
        remaining = int(COOLDOWN_SECONDS - (current_time - LAST_ALERT_TIME))
        print(f"--- Alert suppressed. Cooldown active for {remaining}s ---")
        return

    # If cooldown is over, send the message
    try:
        account_sid = os.getenv('account_sid')
        auth_token = os.getenv('auth_token')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='whatsapp:+14155238886', 
            body=f'🚨 CSI-Cipher Alert: {msg}',
            to='whatsapp:+918219291979' 
        )
        
        LAST_ALERT_TIME = current_time # Reset the timer
        print(f"✅ WhatsApp Sent: {msg}")
    except Exception as e:
        print(f"❌ Failed to send WhatsApp: {e}")

def monitor_live_wifi():
    print("--- CSI-Cipher: SYSTEM ARMED & LIVE ---")
    window_size = 10
    recent_packets = [] 

    while True:
        try:
            if ser.in_waiting > 0:
                line_raw = ser.readline()
                line = line_raw.decode('utf-8', errors='ignore').strip()
                
                # Check for the CSI keyword and ensure the data array is present
                if "CSI_DATA" in line and "[" in line:
                    # Extract numbers from inside the brackets
                    raw_numbers = line.split('[')[1].split(']')[0]
                    
                    # Convert space-separated strings to integers
                    csi_values = [int(x) for x in raw_numbers.split() if x.strip()]
                    
                    if len(csi_values) < 20: continue

                    # We use a stable slice of subcarriers (e.g., 20-25)
                    recent_packets.append(csi_values[20:25])
                    
                    if len(recent_packets) > window_size:
                        recent_packets.pop(0)

                    if len(recent_packets) == window_size:
                        temp_df = pd.DataFrame(recent_packets)
                        # Std Dev detects the "ripple" in the waves caused by movement
                        movement_score = temp_df.std().mean()
                        
                        print(f"Live Score: {movement_score:.4f}")

                        if movement_score > 30: # Threshold calibration
                            print(f"🚨 INTRUDER DETECTED! (Score: {movement_score:.2f})")
                            send_to_whatsapp(f"Security Alert: Movement detected! Score: {movement_score:.2f}")
                            # Optional: Clear window after alert to reset baseline
                            recent_packets = [] 
        
        except Exception as e:
            # If a line is malformed, we just skip it and keep the system running
            continue

if __name__ == "__main__":
    monitor_live_wifi()