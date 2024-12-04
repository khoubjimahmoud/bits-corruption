import pandas as pd
import numpy as np

# Charger les données
bit_data = pd.read_csv(
    r'C:\Users\user\Downloads\bit_static_outdoor_LOS_IUT_1_5890_50_5.csv',
    low_memory=False
)

bit_data.columns = bit_data.columns.str.strip()

data_file = r'C:\Users\user\Downloads\data_static_outdoor_LOS_IUT_1_5890_50_5.csv'
data = pd.read_csv(data_file)
data.columns = data.columns.str.strip()

def extract_first_corrupt_sequence(output_file):
    result_data = []
    
    for _, row in data.iterrows():
        pkt_id = row['pktId']
        time = row['Time']
        
        packet_corrupt_bits = bit_data[bit_data['pktId'] == pkt_id]
        if not packet_corrupt_bits.empty:
            corrupt_bits_only = packet_corrupt_bits.select_dtypes(include=[np.number]).iloc[:, 14:]
            corrupt_bit_array = corrupt_bits_only.values[0]
            
            first_sequence = ""
            start = False
            for bit in corrupt_bit_array:
                if bit == 1:
                    first_sequence += "1"
                    start = True
                elif start:
                    break 
            first_corrupt_bit_pos = np.argmax(corrupt_bit_array) if "1" in first_sequence else None
        else:
            first_sequence = None
            first_corrupt_bit_pos = None

        result_data.append({
            "Time": time,
            "pktId": pkt_id,
            "FirstCorruptBitPosition": first_corrupt_bit_pos,
            "FirstCorruptBitSequence": first_sequence
        })

    result_df = pd.DataFrame(result_data)
    result_df.to_csv(output_file, index=False)
    print(f"Fichier avec les séquences de bits corrompus enregistré dans : {output_file}")

# Spécifiez le chemin du fichier de sortie
output_csv_file = r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\RESULT_CSV\extracted_with_sequences.csv'

extract_first_corrupt_sequence(output_csv_file)
