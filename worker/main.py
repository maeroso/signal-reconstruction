import pandas as pd

g_csv = pd.read_csv('./files/g-1.txt', sep='\n', decimal=',', header=None)
H_csv = pd.read_csv('./files/H-1/H-1.txt', header=None)

H = H_csv.to_numpy()
