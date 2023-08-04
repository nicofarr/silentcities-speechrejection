import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
#### old method by just matching the ratio of rejected files by GPV and AudioSet
Df = pd.read_csv('AllGPV.csv',sep='\t')
Df['duration'] = Df['offset'] - Df['onset']

Df['site'] = [x.split('/')[3] for x in Df['filename']]


Df.sort_values(by='site', inplace=True)
listsites = Df['site'].unique()

#plt.hist(Df['duration'], bins=100)
#plt.show()

Df_speech = pd.read_csv('AllSpeechThresholds.csv')
Df_speech.sort_values(by='site', inplace=True)
listthresholds = np.linspace(0,1,100)

allcomparisons=[]
for cursite in listsites:
    Df_site = Df[Df['site'] == cursite]
    site_ratios = Df_speech[Df_speech['site'] == f"partID{cursite[1:]}"].drop(columns=['site']).to_numpy()

    speechfiles = Df_site['filename'].unique()
    try:

        Df_allfiles_site = pd.read_csv('AcousticMeasurements_renamed/' + f"partID{cursite[1:]}.csv")
        allfiles = Df_allfiles_site['name'].unique()
        ratio = len(speechfiles) / len(allfiles)
        
        # the best threshold is the ratio closest to site_ratios
        best_ratio_ind =[np.argmin(np.abs(site_ratios - ratio))]
        best_thr = listthresholds[best_ratio_ind][0]
        best_ratio = site_ratios[0][best_ratio_ind][0]
        
        print(f"Site {cursite} has {len(speechfiles)} speech files out of {len(allfiles)} files, actual ratio is {ratio} : with AudioSet tagging the best threshold is {best_thr} with a ratio of {best_ratio}")
        
        newnamesite = f"partID{cursite[1:]}"
        allcomparisons.append(dict(site=newnamesite, nfiles = len(allfiles), speechfiles = len(speechfiles),ratio=ratio, best_thr=best_thr, best_ratio=best_ratio,duration_mean=Df_site['duration'].mean(),duration_std=Df_site['duration'].std()))
    except:
        print(f"Problem with site {cursite}")
Df_allcomparisons = pd.DataFrame.from_dict(allcomparisons)
Df_allcomparisons.sort_values(by='ratio').to_csv('AllComparisons.csv', index=False)