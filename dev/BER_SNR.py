import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

bit_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\BIT_CSV\bit_static_outdoor_LOS_IUT_8_5890_50_21.csv')
bit_data.columns = bit_data.columns.str.strip()

status_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\DATA_CSV\data_static_outdoor_LOS_IUT_8_5890_50_21.csv')
status_data.columns = status_data.columns.str.strip()
status_data = status_data[status_data['status'] == 'DATA']

def calculate_ber(row):
    valid_bits = row.dropna()  
    total_bits = len(valid_bits)  
    corrupt_bits = (valid_bits == 1).sum()  
    return corrupt_bits / total_bits if total_bits > 0 else None 

data_rates = [6, 9, 12, 18, 24, 36, 48, 54]

for rate in data_rates:
    rate_data = status_data[status_data['dataRate'] == rate]
    
    # Matching
    common_pkt_ids = np.intersect1d(bit_data['pktId'].values, rate_data['pktId'].values)
    
    # Filter
    filtered_bit_data = bit_data[bit_data['pktId'].isin(common_pkt_ids)].iloc[:, 14:11999]
    filtered_status_data = rate_data[rate_data['pktId'].isin(common_pkt_ids)]
    
    # Group 
    grouped_bit_data = bit_data[bit_data['pktId'].isin(common_pkt_ids)].groupby('pktId').apply(lambda df: df.iloc[:, 14:11999].apply(calculate_ber, axis=1).mean())
    
    snr_values = filtered_status_data['snr'].values
    ber_values = grouped_bit_data.values  
    """
    # Debug
    if len(ber_values) != len(snr_values):
        print(f"Warning: Length mismatch - BER: {len(ber_values)}, SNR: {len(snr_values)} for data rate {rate}")
        continue  # Skip this rate if lengths don't match
    """
    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(snr_values, ber_values, color='skyblue', edgecolor='black')
    plt.title(f'Graphique BER vs SNR pour tous les paquets (dataRate = {rate})')
    plt.xlabel('SNR')
    plt.ylabel('BER')
    plt.grid(True)
    plt.show()