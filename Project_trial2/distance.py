import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv('top.csv')

df = pd.DataFrame(data).set_index('Player')

scaler = MinMaxScaler()
scaled_df = pd.DataFrame(scaler.fit_transform(df), index=df.index, columns=df.columns)

def calculate_euclidean_distance(row, input_data):
    return np.sqrt(np.sum([(row[col] - input_data[col]) ** 2 for col in input_data.keys()]))

def find_closest_player(scaled_df, scaled_gold, scaled_vs, scaled_dmg, scaled_kp, scaled_xpd):
    input_data = {
        'GOLD%': scaled_gold,
        'VS%': scaled_vs,
        'DMG%': scaled_dmg,
        'KP%': scaled_kp,
        'XPD@15': scaled_xpd
    }
    
    distances = scaled_df.apply(calculate_euclidean_distance, axis=1, input_data=input_data)
    similar_player = distances.idxmin() 
    
    return similar_player