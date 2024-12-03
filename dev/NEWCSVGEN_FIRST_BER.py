import pandas as pd
import numpy as np

#CHANGE THE PATHS

bit_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\BIT_CSV\bit_static_outdoor_LOS_IUT_8_5890_50_21.csv')
bit_data.columns = bit_data.columns.str.strip()

#CHANGE THE PATHS
data_file = r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\DATA_CSV\data_static_outdoor_LOS_IUT_8_5890_50_21.csv'
data = pd.read_csv(data_file)
data.columns = data.columns.str.strip()

def calculate_ber_and_save(output_file):
    result_data = []
    total_bits = 12000  

    for _, row in data.iterrows():
        pkt_id = row['pktId']
        status = row['status']
        time = row['Time']
        data_rate = row['dataRate']

        packet_corrupt_bits = bit_data[bit_data['pktId'] == pkt_id]
        if not packet_corrupt_bits.empty:
            corrupt_bits_only = packet_corrupt_bits.select_dtypes(include=[np.number]).iloc[:, 14:]
            num_corrupt_bits = corrupt_bits_only.sum(axis=1).values[0]  
            ber = num_corrupt_bits / total_bits
            first_corrupt_bit_pos = corrupt_bits_only.idxmax(axis=1).values[0]  
        else:
            if status == "DATA":
                corrupt_bits_only = row.iloc[14:]  
                num_corrupt_bits = sum(corrupt_bits_only.values == 1)
                ber = num_corrupt_bits / total_bits
                first_corrupt_bit_pos = None
            elif status == "OK":
                ber = 0
                first_corrupt_bit_pos = None
            elif status == "PHY":
                ber = 1
                first_corrupt_bit_pos = None
            else:
                ber = None
                first_corrupt_bit_pos = None

        result_data.append({
            "Time": time,
            "pktId": pkt_id,
            "FirstCorruptBitPosition": first_corrupt_bit_pos,
            "BER": ber
        })

    result_df = pd.DataFrame(result_data)
    result_df.to_csv(output_file, index=False)
    print(f"Fichier avec BER enregistré dans : {output_file}")

#CHANGE PATH!!!
output_csv_file = r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\RESULT_CSV\extracted_with_ber_8.csv'

calculate_ber_and_save(output_csv_file)
