import pandas
import os
import numpy as np
from matplotlib import pyplot as plt

listcsv = os.listdir('AcousticMeasurements/')
os.makedirs('Thresholds/', exist_ok=True)
listthresholds = np.linspace(0,1,100)


allresults = []
doplot = False
for curcsv in listcsv:
    print(curcsv)
    Df = pandas.read_csv('AcousticMeasurements/' + curcsv)
    
    speech = Df['tag_Talking']
    detected = dict()
    detected['site'] = curcsv[:-4]
    detected['nfiles'] = len(Df['name'].unique())
    for thr in listthresholds:
        Df[f"speech_{thr}"] = speech > thr
        detected[f"speech_{thr}"] = (Df[f"speech_{thr}"].mean())
    
    allresults.append((pandas.DataFrame.from_dict(detected, orient='index').T))
    if doplot:
        plt.plot(listthresholds, detected)
        plt.xlabel('Speech Threshold')
        plt.ylabel('Rejected speech')
        plt.axline((0.2,0), (0.2,1), color='red')
        plt.title(f'site {curcsv[:-4]}')
        plt.show()
        #Df.to_csv('Thresholds/' + curcsv[:-4] + '_thr' + str(thr) + '.csv', index=False)


Df_speech = pandas.concat(allresults)
Df_speech.to_csv('AllSpeechThresholds.csv', index=False)
print(Df_speech)
