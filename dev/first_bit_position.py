import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# First bit position (y axis) PktId (x axis)
# SNR CODE COLORING NOT IMPLEMENTED YET!!!!

bit_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\BIT_CSV\bit_static_outdoor_LOS_IUT_1_5890_50_5.csv')
bit_data.columns = bit_data.columns.str.strip()

def plot_first_corrupt_bit(data_rate):
    filtered_status_data = bit_data[bit_data['dataRate'] == data_rate]
    
    if filtered_status_data.empty:
        print(f"Aucune trame trouvée pour le dataRate = {data_rate}")
        return
    
    filtered_bit_data = filtered_status_data.groupby('pktId').first().reset_index()
    corrupt_bits_only = filtered_bit_data.iloc[:, 14:]

    def find_first_corrupt_bit(row):
        valid_bits = row.dropna().values 
        one_indices = np.where(valid_bits == 1)[0]  
        return one_indices[0] if one_indices.size > 0 else None
        
    first_corrupt_positions = corrupt_bits_only.apply(find_first_corrupt_bit, axis=1).values
    pkt_ids = filtered_bit_data['pktId'].values  
    """
    DEBUG
    print(first_corrupt_positions)
    print(pkt_ids)
    """
    positions_filtered = [pos for pos in first_corrupt_positions if pos is not None]
    pkt_ids_filtered = [pkt_id for pos, pkt_id in zip(first_corrupt_positions, pkt_ids) if pos is not None]
    """
    DEBUG
    print(positions_filtered)
    print(pkt_ids_filtered)
    """
    
    plt.figure(figsize=(10, 6))
    plt.scatter(pkt_ids_filtered, positions_filtered, color='skyblue', edgecolors='black')
    plt.title(f"Position du premier bit corrompu ('1') par trame pour DataRate = {data_rate}")
    plt.xlabel('pktId')
    plt.ylabel('Position du premier bit corrompu')
    plt.grid(True)
    plt.show()


plot_first_corrupt_bit(6)

plot_first_corrupt_bit(9)
plot_first_corrupt_bit(12)
plot_first_corrupt_bit(18)
plot_first_corrupt_bit(24)
plot_first_corrupt_bit(36)
plot_first_corrupt_bit(48)
plot_first_corrupt_bit(54)