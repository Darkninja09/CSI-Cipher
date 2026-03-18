import pandas as pd
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv('data.csv') 
def monitor_wifi_signals(data):
        print("--- CSI-Cipher Security: Monitoring Live WiFi Signals ---")
        
        
        for i in range(10, len(data)):
            
            window = data.iloc[i-10:i, 0:5] 
            

            movement_score = window.std().mean()
            

            if movement_score > 5.0:
                print(f"!!! INTRUDER DETECTED at index {i} (Score: {movement_score:.2f}) !!!")
                send_to_whatsapp('movement detected')
                
                break
                
            time.sleep(0.05) 

        monitor_wifi_signals(df)

def monitor_room_csv(data_frame):
    print("System Armed: Monitoring WiFi signals...")

    baseline = data_frame.iloc[0, 0] 
    
    for index, row in data_frame.iterrows():
        current_signal = row.iloc[30] 
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
    from_='whatsapp:+14155238886', 
    body='🚨 WiFi Sensor Alert: Movement detected!',
    to='whatsapp:+918219291979' 
    )
    print(f"Success: {msg}")

monitor_room_csv(df)