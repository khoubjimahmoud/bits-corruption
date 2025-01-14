# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 20:46:15 2025

@author: AKRAM
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# Chargement des données
bit_data = pd.read_csv(r'C:\Users\user\Downloads\bit_static_outdoor_LOS_IUT_1_5890_50_5.csv')
bit_data.columns = bit_data.columns.str.strip()

status_data = pd.read_csv(r'C:\Users\user\Downloads\data_static_outdoor_LOS_IUT_1_5890_50_5.csv')
status_data.columns = status_data.columns.str.strip()

def group_peaks(peaks, distance_threshold=50):
    """
    Regrouper les positions proches en une seule position représentative.
    :param peaks: Liste des positions des pics détectés.
    :param distance_threshold: Distance maximale entre deux pics pour les regrouper.
    :return: Liste des positions regroupées.
    """
    grouped_peaks = []
    peaks.sort()
    current_group = [peaks[0]]

    for peak in peaks[1:]:
        if peak - current_group[-1] <= distance_threshold:
            current_group.append(peak)
        else:
            grouped_peaks.append(int(np.mean(current_group)))  # Moyenne des positions du groupe
            current_group = [peak]

    # Ajouter le dernier groupe
    if current_group:
        grouped_peaks.append(int(np.mean(current_group)))

    return grouped_peaks

# Supposons que bit_corruption_freq est global ou calculé dans plot_bit_corruption.
bit_corruption_freq = None  # À calculer dans plot_bit_corruption

def plot_bit_corruption(data_rate, ax):
    global bit_corruption_freq  # Rendre accessible à l'extérieur
    # Filtrer les paquets corrompus pour le débit binaire donné
    corrupt_packets = status_data[(status_data['status'] == 'DATA') & (status_data['dataRate'] == data_rate)]['pktId']
    print(f"Number of corrupted packets for {data_rate} Mb/s: {len(corrupt_packets)}")
    
    # Extraire les données des bits pour ces paquets
    corrupt_bit_data = bit_data[bit_data['pktId'].isin(corrupt_packets)]
    corrupt_bits = corrupt_bit_data.iloc[:, 14:]
    corrupt_bits = corrupt_bits.apply(pd.to_numeric, errors='coerce')
    
    # Calculer la fréquence de corruption des bits
    bit_corruption_count = (corrupt_bits == 1).sum(axis=0)
    total_packets = len(corrupt_packets)
    if total_packets > 0:
        bit_corruption_freq = bit_corruption_count / total_packets
    else:
        bit_corruption_freq = np.zeros(corrupt_bits.shape[1])
    
    # Détection des pics sans contrainte de distance
    peaks, properties = find_peaks(bit_corruption_freq, height=0.095)  # Seuil minimum pour les pics
    
    # Regrouper les pics proches
    grouped_peaks = group_peaks(peaks, distance_threshold=50)
    print(f"Grouped Peaks (unique positions): {grouped_peaks}")
    
    # Tracer la fréquence de corruption des bits
    ax.scatter(range(len(bit_corruption_freq)), bit_corruption_freq, s=1, color='black', label='Frequency')

    # Tracer les pics regroupés
    ax.scatter(grouped_peaks, bit_corruption_freq[grouped_peaks], color='blue', label='Grouped Peaks', s=100)
    
    ax.set_xlabel('Bit Position')
    ax.set_ylabel('Normalized Bit Corruption Frequency')
    ax.set_title(f'1500 bytes ({data_rate} Mb/s)')
    ax.legend()
    return grouped_peaks

# Tracer pour le débit 18 Mbps
fig, ax = plt.subplots(1, 1, figsize=(14, 6))
grouped_peaks = plot_bit_corruption(18, ax)
plt.tight_layout()
plt.show()

