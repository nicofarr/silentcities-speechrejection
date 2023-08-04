import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
import sklearn.metrics

nploader = np.load('gpv_tagging_results.npz')#, allfpr=allfpr, alltpr=alltpr, listthresholds=listthresholds, ratios_noGPV=ratios_noGPV)

allfpr = nploader['allfpr']
alltpr = nploader['alltpr']
listthresholds = nploader['listthresholds']
ratios_noGPV = nploader['ratios_noGPV']

# plot of all ROC curves with a confidence interval according to the first dimension of allfpr and alltpr
plt.figure()
for i in range(allfpr.shape[0]):
    plt.plot(allfpr[i], alltpr[i], color='grey', alpha=0.2)

medianfpr = np.median(allfpr, axis=0)
mediantpr = np.median(alltpr, axis=0)

chosen_tpr = 0.75
# find the closest tpr to the chosen one
closest_ind = np.argmin(np.abs(mediantpr - chosen_tpr))
# find the corresponding fpr
chosen_fpr = medianfpr[closest_ind]

print(f"Chosen FPR: {chosen_fpr:.2f} for TPR={chosen_tpr:.2f}, for a threshold of {listthresholds[closest_ind]:.2f}")

# find the closest value to chosen_tpr in listthresholds
closest_ind = np.argmin(np.abs(listthresholds - listthresholds[closest_ind]))
print(f"Chosen threshold: {listthresholds[closest_ind]:.2f} for TPR={chosen_tpr:.2f}, for a FPR of {medianfpr[closest_ind]:.2f}")

final_thr = listthresholds[closest_ind]

os.makedirs('AcousticMeasurements_renamed_withspeech/', exist_ok=True)


Df = pd.read_csv('AllGPV.csv',sep='\t')
Df['site'] = [x.split('/')[3] for x in Df['filename']]
Df.sort_values(by='site', inplace=True)
listsites = Df['site'].unique()
listsites2 = ['partID' + x[1:] for x in listsites]
#plt.hist(Df['duration'], bins=100)
#plt.show()

Df_speech = pd.read_csv('AllSpeechThresholds.csv')
Df_speech.sort_values(by='site', inplace=True)
sitelist = ['partID' + x[6:].zfill(3) for x in Df_speech['site']]

# new list of sites correspond to sites of sitelist which are not in listsites2
listsites_noGPV = [x for x in sitelist if x not in listsites2]



for curfile in listsites_noGPV:
    sitefile = os.path.join('AcousticMeasurements_renamed/',curfile + '.csv')
    sitenum = '0'+curfile.split('.')[0][6:]

    Dfacoustic = pd.read_csv(sitefile)
    Dfacoustic['reject_speech'] = 0
    Dfacoustic.loc[Dfacoustic['tag_Talking'] > final_thr, 'reject_speech'] = 1

    Dfacoustic['filename_short'] = [os.path.split(x)[1] for x in Dfacoustic['name']]

    Dfacoustic.to_csv(os.path.join('AcousticMeasurements_renamed_withspeech/',curfile+ '.csv'), index=False)