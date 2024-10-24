import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Path!!
bit_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bit-csv\bit_static_outdoor_LOS_IUT_8_5890_50_21.csv')
bit_data.columns = bit_data.columns.str.strip()

status_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bit-csv\data_static_outdoor_LOS_IUT_8_5890_50_21.csv')
status_data.columns = status_data.columns.str.strip()

def plot_bit_corruption(data_rate, ax):
    
    corrupt_packets = status_data[(status_data['status'] == 'DATA') & (status_data['dataRate'] == data_rate)]['pktId']
    print(f"Number of corrupted packets for {data_rate} Mb/s: {len(corrupt_packets)}")
    
    corrupt_bit_data = bit_data[bit_data['pktId'].isin(corrupt_packets)]
    corrupt_bits = corrupt_bit_data.iloc[:, 14:]
    
    corrupt_bits = corrupt_bits.apply(pd.to_numeric, errors='coerce')
    
    bit_corruption_count = (corrupt_bits == 1).sum(axis=0)
    total_packets = len(corrupt_packets) 
    
    if total_packets > 0:
        bit_corruption_freq = bit_corruption_count / total_packets
    else:
        bit_corruption_freq = np.zeros(corrupt_bits.shape[1])
    
    ax.scatter(range(len(bit_corruption_freq)), bit_corruption_freq, s=1, color='black')
    ax.set_xlabel('Bit Position')
    ax.set_ylabel('Normalized Bit Corruption Frequency')
    ax.set_title(f'1500 bytes ({data_rate} Mb/s)')

fig, axes = plt.subplots(1, 8, figsize=(28, 6))

# Tout les DataRates -->
plot_bit_corruption(6, axes[0])
plot_bit_corruption(9, axes[1])
plot_bit_corruption(12, axes[2])
plot_bit_corruption(18, axes[3])
plot_bit_corruption(24, axes[4])
plot_bit_corruption(36, axes[5])
plot_bit_corruption(48, axes[6])
plot_bit_corruption(54, axes[7]) 

plt.tight_layout()

plt.show()
