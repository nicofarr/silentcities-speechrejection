import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
import sklearn.metrics

Df = pd.read_csv('AllGPV.csv',sep='\t')
Df['duration'] = Df['offset'] - Df['onset']

Df['site'] = [x.split('/')[3] for x in Df['filename']]


Df.sort_values(by='site', inplace=True)
listsites = Df['site'].unique()
listsites2 = ['partID' + x[1:] for x in listsites]
#plt.hist(Df['duration'], bins=100)
#plt.show()

Df_speech = pd.read_csv('AllSpeechThresholds.csv')
Df_speech.sort_values(by='site', inplace=True)
sitelist = ['partID' + x[6:].zfill(3) for x in Df_speech['site']]
Df_speech['site'] = sitelist

# new list of sites correspond to sites of sitelist which are not in listsites2
listsites_noGPV = [x for x in sitelist if x not in listsites2]

ratios_noGPV = []
for cursite in listsites_noGPV:    
    Df_speech_site = Df_speech[Df_speech['site'] == cursite]
    siteratios = Df_speech_site.drop(columns=['site','nfiles']).to_numpy()
    ratios_noGPV.append(siteratios)

ratios_noGPV = np.concatenate(ratios_noGPV)
listthresholds = np.linspace(0,1,100)

os.makedirs('roc_GPV_audioset/', exist_ok=True)

allfpr = []
alltpr = []

allcomparisons=[]
for cursite in listsites:
    try:
        Df_site = Df[Df['site'] == cursite]
        site_ratios = Df_speech[Df_speech['site'] == f"partID{cursite[1:]}"].drop(columns=['site']).to_numpy()
        Df_speech_site = Df_speech[Df_speech['site'] == f"partID{cursite[1:]}"]
        siteratios = Df_speech_site.drop(columns=['site','nfiles']).to_numpy()

        speechfiles = Df_site['filename'].unique()
        ntotalfiles =Df_speech_site['nfiles'].to_numpy()[0]
        

        Df_allfiles_site = pd.read_csv('AcousticMeasurements_renamed_withspeech/' + f"partID{cursite[1:]}.csv")
        
        y_true = Df_allfiles_site['reject_speech']
        y_pred = Df_allfiles_site['tag_Talking']
        ngpv = len(y_true[y_true == 1])
        if ngpv == 0:
            print(f"Site {cursite} does not have any positive speech detection by GPV, skipping")
            continue

        fpr, tpr, thresholds = sklearn.metrics.roc_curve(y_true=y_true, y_score=y_pred)
        
        #find closest values of listthresholds in thresolds
        closest_ind = np.argmin(np.abs(thresholds[:,np.newaxis] - listthresholds), axis=0)



        roc_auc = sklearn.metrics.auc(fpr, tpr)
        display = sklearn.metrics.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc)
        display.plot()
        plt.savefig('roc_GPV_audioset/roccurve_' + f"partID{cursite[1:]}.png")
        plt.close()

        # Plot curves of FPR and TPR as a function of ratios
        plt.plot(siteratios[0], fpr[closest_ind])
        plt.plot(siteratios[0], tpr[closest_ind])
        plt.xlabel('Ratio of rejected files')
        plt.title(f"Site {cursite}, AUC={roc_auc:.2f}, nGPV={ngpv} on a total of {ntotalfiles}")
        plt.legend(['FPR', 'TPR'])        
        plt.savefig('roc_GPV_audioset/ratios_' + f"partID{cursite[1:]}.png")
        plt.close()


        ### Aggreggating FPR and TPR for sites with more than a 1000 files 
        if ntotalfiles > 1000:
            allfpr.append(fpr[closest_ind])
            alltpr.append(tpr[closest_ind])                
    except Exception as e:
        print(f"Problem with site {cursite}")
        print(e)





np.savez_compressed('gpv_tagging_results.npz', allfpr=allfpr, alltpr=alltpr, listthresholds=listthresholds, ratios_noGPV=ratios_noGPV)
allfpr = np.array(allfpr)
alltpr = np.array(alltpr)
medianfpr = np.median(allfpr, axis=0)
mediantpr = np.median(alltpr, axis=0)

plt.subplot(3,2,1)
plt.plot(medianfpr, mediantpr)
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('Median ROC curve (GT)')

plt.subplot(3,2,2)
plt.plot(listthresholds, mediantpr)
plt.xlabel('threshold')
plt.ylabel('TPR')
plt.title('Median TPR curve (GT)')

plt.subplot(3,2,3)
plt.plot(listthresholds, medianfpr)
plt.xlabel('threshold')
plt.ylabel('FPR')
plt.title('Median FPR curve (GT)')


plt.subplot(3,2,4)
plt.plot(np.mean(ratios_noGPV,axis=0),mediantpr)
plt.xlabel('Rejected files ratio')
plt.ylabel('TPR (est)')

plt.subplot(3,2,5)
plt.plot(np.mean(ratios_noGPV,axis=0),medianfpr)
plt.xlabel('Rejected files ratio')
plt.ylabel('FPR (est)')

plt.savefig('roc_GPV_audioset/median_roc_ratios.png')