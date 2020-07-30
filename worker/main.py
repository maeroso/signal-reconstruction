import numpy as np
import pandas as pd
import time

start = time.time()

g_csv = pd.read_csv('./files/g-1.txt', sep='\n',
                    decimal=',', header=None, dtype=float)

end = time.time()
print('Carregando csv do vetor g -> Minutos: ' + str(int((end - start) / 60)) +
      '   Segundos: ' + str(int((end - start) / 60)))
start = time.time()

H_csv = pd.read_csv('./files/H-1/H-1.txt', header=None, dtype=float)

end = time.time()
print('Carregando csv da matrix H -> Minutos: ' + str(int((end - start) / 60)) +
      '   Segundos: ' + str(int((end - start) / 60)))
start = time.time()

H = H_csv.to_numpy()

end = time.time()
print('Convertendo csv da matrix H para o formato da biblioteca numpy -> Minutos: ' + str(int((end - start) / 60)) +
      '   Segundos: ' + str(int((end - start) / 60)))
start = time.time()

g = g_csv.to_numpy()

end = time.time()
print('Convertando csv do vetor g para o formato da biblioteca numpy -> Minutos: ' + str(int((end - start) / 60)) +
      '   Segundos: ' + str(int((end - start) / 60)))
start = time.time()


print('Cheguei aqui')

p0 = np.matmul(H.transpose(), g)
