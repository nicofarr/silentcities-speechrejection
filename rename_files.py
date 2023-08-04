import pandas
import os
import numpy as np
from matplotlib import pyplot as plt
import shutil

listcsv = os.listdir('AcousticMeasurements/')
os.makedirs('AcousticMeasurements_renamed/', exist_ok=True)

for curcsv in listcsv:
    sitenum = curcsv.split('.')[0][6:]
    #newname is partID_sitenum with sitenum on three digits
    newname = curcsv.split('.')[0][:6] + sitenum.zfill(3) + '.csv'
    shutil.copyfile('AcousticMeasurements/' + curcsv, 'AcousticMeasurements_renamed/' + newname)