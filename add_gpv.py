import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt

Df = pd.read_csv('AllGPV.csv',sep='\t')

os.makedirs('AcousticMeasurements_renamed_withspeech/', exist_ok=True)

## add the site column by extracting it from the filename. Prototype is /bigdisk1/silentcities/0117/ + filename and the site name is 0117
Df['site'] = [x.split('/')[3] for x in Df['filename']]

csvfiles = os.listdir('AcousticMeasurements_renamed/')

for curfile in csvfiles:
    sitefile = os.path.join('AcousticMeasurements_renamed/',curfile)
    sitenum = '0'+curfile.split('.')[0][6:]
    
    #get the corresponding rows in Df
    Dfsite = Df.loc[Df['site'] == sitenum]

    if len(Dfsite) == 0:
        print(f'No GPV detections were made for site {sitenum}')
        continue

    Dfacoustic = pd.read_csv(sitefile)
    Dfacoustic['reject_speech'] = 0
    
    # Generate columns in both dataframes with only the file name 
    Dfsite['filename_short'] = [os.path.split(x)[1] for x in Dfsite['filename']]
    Dfacoustic['filename_short'] = [os.path.split(x)[1] for x in Dfacoustic['name']]

    # Put 1 in the reject_speech column of Dfacoustic if the corresponding filename is in Dfsite
    Dfacoustic.loc[Dfacoustic['filename_short'].isin(Dfsite['filename_short']), 'reject_speech'] = 1

    Dfacoustic.to_csv(os.path.join('AcousticMeasurements_renamed_withspeech/',curfile), index=False)