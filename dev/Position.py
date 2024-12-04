import pandas as pd
import matplotlib.pyplot as plt

#NOT FINISHED!!!
#NOT FINISHED!!!
#NOT FINISHED!!!#NOT FINISHED!!!#NOT FINISHED!!!#NOT FINISHED!!!
#NOT FINISHED!!!
#NOT FINISHED!!!
#NOT FINISHED!!!
#NOT FINISHED!!!
#NOT FINISHED!!!#NOT FINISHED!!!#NOT FINISHED!!!#NOT FINISHED!!!#NOT FINISHED!!!#NOT FINISHED!!!


bit_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\BIT_CSV\bit_static_outdoor_LOS_IUT_1_5890_50_5.csv')
#status_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\DATA_CSV\data_static_outdoor_LOS_IUT_1_5890_50_5.csv')

bit_data.columns = bit_data.columns.str.strip()
#status_data.columns = status_data.columns.str.strip()

def plot_last_corrupt_bit(data_rate):
    filtered_status_data = bit_data[bit_data['dataRate'] == data_rate]
    
    if filtered_status_data.empty:
        print(f"Aucune trame trouvée pour le dataRate = {data_rate}")
        return
    
    filtered_pkt_ids = filtered_status_data['pktId'].values
    print(f"Nombre de trames trouvées pour le dataRate = {data_rate} : {len(filtered_pkt_ids)}")
    
    filtered_bit_data = bit_data[bit_data['pktId'].isin(filtered_pkt_ids)]
    
    corrupt_bits_only = filtered_bit_data.iloc[:, 14:]
    
   
    
    def find_last_corrupt_bit(row):
        #valid_bits = row.dropna() 
        valid_bits = row
        last_one_index = valid_bits[valid_bits == 1].last_valid_index()  
        return int(last_one_index) if last_one_index is not None else None
        
    
    last_corrupt_positions = corrupt_bits_only.apply(find_last_corrupt_bit, axis=1).values
    pkt_ids = filtered_bit_data['pktId'].values  
    print(last_corrupt_positions)
    print(pkt_ids)
    
    
    positions_filtered = [pos for pos in last_corrupt_positions if pos is not None]
    pkt_ids_filtered = [pkt_id for pos, pkt_id in zip(last_corrupt_positions, pkt_ids) if pos is not None]
    
    print(positions_filtered)
    print(pkt_ids_filtered)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(pkt_ids_filtered, positions_filtered, color='skyblue', edgecolors='black')
    plt.title(f"Position du dernier bit corrompu ('1') par trame pour DataRate = {data_rate}")
    plt.xlabel('pktId')
    plt.ylabel('Position du dernier bit corrompu')
    plt.grid(True)
    plt.show()

plot_last_corrupt_bit(6)
"""
plot_last_corrupt_bit(9)
plot_last_corrupt_bit(12)
plot_last_corrupt_bit(18)
plot_last_corrupt_bit(24)
plot_last_corrupt_bit(36)
plot_last_corrupt_bit(48)
plot_last_corrupt_bit(54)
"""
