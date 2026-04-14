import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# Files to monitor
CSI_FILE = "csi_data.csv"
LABEL_FILE = "label_boxes.csv"

def animate(i):
    if not os.path.exists(CSI_FILE):
        return

    try:
        # Read CSI Data
        csi_df = pd.read_csv(CSI_FILE)
        if csi_df.empty:
            return
            
        csi_data = csi_df.iloc[-50:, 1:].values
        
        # Read Label/Box Data (Simulating Prediction or ground truth)
        label_df = pd.read_csv(LABEL_FILE)
        
        plt.clf()
        
        # Subplot 1: CSI Heatmap (The Signal)
        ax1 = plt.subplot(1, 2, 1)
        im = ax1.imshow(csi_data, aspect='auto', cmap='viridis', interpolation='nearest')
        ax1.set_title("Wi-Fi Signal (CSI Heatmap)")
        ax1.set_xlabel("Subcarrier")
        ax1.set_ylabel("Time")
        
        # Subplot 2: Human Position (The Movement)
        ax2 = plt.subplot(1, 2, 2)
        if not label_df.empty:
            # We use the row index to simulate "live" movement from the labels
            # In a real scenario, this would be the output of your ML model
            idx = (i * 5) % len(label_df) 
            x = label_df.iloc[idx]['x']
            y = label_df.iloc[idx]['y']
            
            # Map coordinates to a representative room space
            ax2.scatter(x, y, color='red', s=100, label='Human')
            ax2.set_xlim(-50, 600) # Based on CSV values seen
            ax2.set_ylim(-50, 600)
            ax2.set_title(f"Live Position: ({x}, {y})")
            ax2.grid(True)
            ax2.legend()

        plt.tight_layout()
        
    except Exception as e:
        print(f"Error updating plot: {e}")

def start_visualization():
    fig = plt.figure(figsize=(12, 5))
    ani = FuncAnimation(fig, animate, interval=100, cache_frame_data=False)
    plt.show()

if __name__ == "__main__":
    start_visualization()
