# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 15:02:51 2024

@author: ASUS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Charger les PATH des CSV!!
bit_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bit-csv\bit_static_outdoor_LOS_IUT_8_5890_50_21.csv')
bit_data.columns = bit_data.columns.str.strip()

status_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bit-csv\data_static_outdoor_LOS_IUT_8_5890_50_21.csv')
status_data.columns = status_data.columns.str.strip()

def longest_corrupted_sequence(bits):
    # Fonction pour calculer la plus longue séquence consécutive de '1' dans une trame donnée.
    
    max_len = 0
    current_len = 0
    for bit in bits:
        if bit == 1:
            current_len += 1  #
            max_len = max(max_len, current_len)  
        else:
            current_len = 0 
    return max_len

def compute_longest_corrupted_sequence_per_frame(data_rate):
    # Calcule la plus longue séquence de bits corrompus consécutifs pour chaque trame.
    
    if status_data['dataRate'].dtype != 'object':
        data_rate = float(data_rate) 
    
    corrupt_packets = status_data[(status_data['status'] == 'DATA') & (status_data['dataRate'] == data_rate)]['pktId']
    print(f"Nombre de trames corrompues pour dataRate={data_rate} : {len(corrupt_packets)}")
    
    corrupt_bit_data = bit_data[bit_data['pktId'].isin(corrupt_packets)]
    
    pktIds = corrupt_bit_data['pktId']  
    corrupt_bits = corrupt_bit_data.iloc[:, 14:]  
    corrupt_bits = corrupt_bits.apply(pd.to_numeric, errors='coerce')  
    
    longest_sequences = corrupt_bits.apply(longest_corrupted_sequence, axis=1)
    
    results = pd.DataFrame({'pktId': pktIds, 'longest_corrupted_sequence': longest_sequences})
    
    print(results)
    
    return results

# EXEMPLE POUR 24 Mb/s 
longest_corrupted_sequences = compute_longest_corrupted_sequence_per_frame('24')

# PREVIEW
print(longest_corrupted_sequences.head())

# Cette ligne est optionnelle
#longest_corrupted_sequences.to_csv('longest_corrupted_sequences.csv', index=False)

longest_corrupted_sequences_sorted = longest_corrupted_sequences.sort_values(by='longest_corrupted_sequence', ascending=False)

plt.figure(figsize=(15, 8))
plt.bar(longest_corrupted_sequences_sorted['pktId'], longest_corrupted_sequences_sorted['longest_corrupted_sequence'], color='skyblue', edgecolor='black')
plt.title('Longueur maximale des séquences corrompues par trame pour dataRate=24 Mb/s')
plt.xlabel('ID des trames (pktId)')
plt.ylabel('Longueur maximale des séquences corrompues')
plt.xticks(rotation=90)  
plt.grid(True)
plt.tight_layout()
plt.show()
