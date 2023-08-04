import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt

Df = pd.read_csv('AllGPV.csv',sep='\t')
Df['duration'] = Df['offset'] - Df['onset']

Df['site'] = [x.split('/')[3] for x in Df['filename']]


Df.sort_values(by='duration', inplace=True)
print(Df.iloc[:10])
#extract the 10 longest and shortest files

longest = (Df.iloc[-10:]['filename'].to_list())
shortest = (Df.iloc[:10]['filename'].to_list())

#prepend /home/nfarrugi to all elements of longest and shortest
longest2 = ['/home/nfarrugi/' + i for i in longest]
shortest2 = ['/home/nfarrugi/' + i for i in shortest]

#copy them to a new folder
os.makedirs('Longest/', exist_ok=True)
os.makedirs('Shortest/', exist_ok=True)

for curfile in longest2:
    os.system(f"cp {curfile} Longest/")
for curfile in shortest2:
    os.system(f"cp {curfile} Shortest/")

