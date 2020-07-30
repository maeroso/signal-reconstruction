import numpy as np
import pandas as pd

g_csv = pd.read_csv('./files/g-1.txt', sep='\n', decimal=',', header=None, dtype=float)
H_csv = pd.read_csv('./files/H-1/H-1.txt', header=None,dtype=float)

H = H_csv.to_numpy()

print('Cheguei aqui')