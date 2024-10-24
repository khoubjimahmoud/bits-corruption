# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:56:23 2024

@author: ASUS
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

bit_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bit-csv\bit_static_outdoor_LOS_IUT_1_5890_50_5.csv')
bit_data.columns = bit_data.columns.str.strip()

status_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bit-csv\data_static_outdoor_LOS_IUT_1_5890_50_5.csv')
status_data.columns = status_data.columns.str.strip()

def plot_corrupted_bits_per_frame():
    corrupt_packets = status_data[status_data['status'] == 'DATA']['pktId']
    print(f"Number of corrupted packets: {len(corrupt_packets)}")
    
    corrupt_bit_data = bit_data[bit_data['pktId'].isin(corrupt_packets)]
    
    pktIds = corrupt_bit_data['pktId']  
    corrupt_bits = corrupt_bit_data.iloc[:, 14:]  
    
    corrupt_bits = corrupt_bits.apply(pd.to_numeric, errors='coerce')
    corrupted_bits_per_frame = (corrupt_bits == 1).sum(axis=1)  
    
    plt.figure(figsize=(10, 6))
    plt.bar(pktIds, corrupted_bits_per_frame, color='skyblue', edgecolor='black')
    plt.title(f'Nombre de bits corrompus par trame')
    plt.xlabel('ID des trames (pktId)')
    plt.ylabel('Nombre de bits corrompus')
    plt.ylim(6000, None) 
   
    plt.grid(True)
    plt.show()

plot_corrupted_bits_per_frame()