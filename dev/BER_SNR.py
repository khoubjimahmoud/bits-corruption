import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
bit_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\BIT_CSV\bit_static_outdoor_LOS_IUT_1_5890_50_5.csv')
bit_data.columns = bit_data.columns.str.strip()

status_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\DATA_CSV\data_static_outdoor_LOS_IUT_1_5890_50_5.csv')
status_data.columns = status_data.columns.str.strip()
status_data = status_data[status_data['status'] == 'DATA']

# BER calculation function
def calculate_ber(row):
    valid_bits = row.dropna()  
    total_bits = len(valid_bits)  
    corrupt_bits = (valid_bits == 1).sum()  
    return corrupt_bits / total_bits if total_bits > 0 else None 

# Data rates to iterate over
data_rates = [6, 9, 12, 18, 24, 36, 48, 54]

# Loop over each data rate and plot log10(BER) vs. SNR
for rate in data_rates:
    rate_data = status_data[status_data['dataRate'] == rate]
    
    # Find common pktIds
    common_pkt_ids = np.intersect1d(bit_data['pktId'].values, rate_data['pktId'].values)
    
    # Filter data
    filtered_bit_data = bit_data[bit_data['pktId'].isin(common_pkt_ids)].iloc[:, 14:]
    filtered_status_data = rate_data[rate_data['pktId'].isin(common_pkt_ids)]
    
    # Group and calculate BER
    grouped_bit_data = bit_data[bit_data['pktId'].isin(common_pkt_ids)].groupby('pktId').apply(lambda df: df.iloc[:, 14:].apply(calculate_ber, axis=1).mean())
    
    # Retrieve SNR values and convert BER values to log10
    snr_values = filtered_status_data['snr'].values
    ber_values = grouped_bit_data.values  
    log_ber_values = np.log10(ber_values)  # Apply log10 transformation to BER values

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(snr_values, log_ber_values, color='skyblue', edgecolor='black')
    plt.title(f'Graphique log10(BER) vs SNR pour tous les paquets (dataRate = {rate})')
    plt.xlabel('SNR')
    plt.ylabel('log10(BER)')
    plt.grid(True)
    
    # Invert the x-axis (SNR) so it starts from the highest value
    plt.gca().invert_xaxis()
    
    # Show the plot
    plt.show()
