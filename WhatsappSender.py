import pandas as pd
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv('data.csv') 
def monitor_wifi_signals(data):
        print("--- DarkBot Security: Monitoring Live WiFi Signals ---")
        
        # We'll use a 'sliding window' of 10 rows to calculate stability
        for i in range(10, len(data)):
            # Get the last 10 snapshots of signal amplitude
            window = data.iloc[i-10:i, 0:5] # Checking first 5 subcarriers
            
            # Calculate 'Movement Score' using Standard Deviation
            # Higher SD = more movement/chaos in the signal
            movement_score = window.std().mean()
            
            # Threshold: 2.0 is usually a 'quiet' room. 
            # If it goes above 5.0, it means the signal is being disrupted by a human.
            if movement_score > 5.0:
                print(f"!!! INTRUDER DETECTED at index {i} (Score: {movement_score:.2f}) !!!")
                send_to_whatsapp('movement detected')
                # --- TRIGGER YOUR WHATSAPP BOT HERE ---
                # send_whatsapp_alert("🚨 Alert: Someone just entered your room!")
                
                break # Stop for now so you don't spam your phone
                
            time.sleep(0.05) # Simulate the speed of real Wi-Fi packets

        monitor_wifi_signals(df)

def monitor_room_csv(data_frame):
    print("System Armed: Monitoring WiFi signals...")

    baseline = data_frame.iloc[0, 0] 
    
    for index, row in data_frame.iterrows():
        current_signal = row.iloc[30] # Signal from the first subcarrier
        change = abs(current_signal - baseline)

        if change > 15:
            print(f"Movement detected at row {index}!")
            send_to_whatsapp("🚨 DarkBot Security: Person detected entering the room!")
            break 
        
        time.sleep(0.1) 

def send_to_whatsapp(msg):
    from twilio.rest import Client

    account_sid = os.getenv('account_sid')
    auth_token = os.getenv('auth_token')


    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886', # Twilio Sandbox Number
    body='🚨 WiFi Sensor Alert: Movement detected!',
    to='whatsapp:+918219291979' # Your verified number
    )
    print(f"Success: {msg}")

monitor_room_csv(df)