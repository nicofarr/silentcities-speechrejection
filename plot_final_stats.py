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

print(f"Chosen FPR: {chosen_fpr:.2f} for TPR={chosen_tpr:.2f}, for a threshold of {listthresholds[::-1][closest_ind]:.2f}")

# find the closest value to chosen_tpr in listthresholds
closest_ind = np.argmin(np.abs(listthresholds[::-1] - listthresholds[::-1][closest_ind]))
print(f"Chosen threshold: {listthresholds[::-1][closest_ind]:.2f} for TPR={chosen_tpr:.2f}, for a FPR of {medianfpr[closest_ind]:.2f}")


plt.subplot(3,2,1)
plt.plot(medianfpr, mediantpr)
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('Median ROC curve (GT)')

plt.subplot(3,2,2)
plt.plot(listthresholds[::-1], mediantpr)
plt.xlabel('threshold')
plt.ylabel('TPR')
plt.title('Median TPR curve (GT)')

plt.subplot(3,2,3)
plt.plot(listthresholds[::-1], medianfpr)
plt.xlabel('threshold')
plt.ylabel('FPR')
plt.title('Median FPR curve (GT)')


plt.subplot(3,2,4)
plt.plot(np.median(ratios_noGPV,axis=0),mediantpr)
plt.xlabel('Rejected files ratio')
plt.ylabel('TPR (est)')

plt.subplot(3,2,5)
plt.plot(np.median(ratios_noGPV,axis=0),medianfpr)
plt.xlabel('Rejected files ratio')
plt.ylabel('FPR (est)')
plt.tight_layout()
plt.savefig('roc_GPV_audioset/median_roc_ratios.png')