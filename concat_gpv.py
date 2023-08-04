import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt

listgpv = os.listdir('/home/nfarrugi/tmpdisk/sl_speechpreds/')

allgpv = []

for curfile in listgpv:
    #check if the file is a csv
    if curfile[-4:] == '.csv':
        allgpv.append(pd.read_csv('/home/nfarrugi/tmpdisk/sl_speechpreds/' + curfile))


Df_gpv = pd.concat(allgpv)
Df_gpv.to_csv('AllGPV.csv', index=False)