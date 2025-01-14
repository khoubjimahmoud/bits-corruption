# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:32:29 2024

@author: ASUS
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

bit_data = pd.read_csv(r'C:\Users\ASUS\Desktop\bits-corruption-Py\data\BIT_CSV\bit_static_outdoor_LOS_IUT_8_5890_50_21.csv')
bit_data.columns = bit_data.columns.str.strip()

print(bit_data.head)