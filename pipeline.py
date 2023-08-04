# sequence of scripts to run to perform GPV statistics and estimation on unseen sites 

# 0. rename_files.py
# 1. concat_gpv.py -> AllGPV.csv
# 2. add_gpv.py -> -> will rewrite the AcousticMeasurements files in a new folder AcousticMeasurements_renamed_withspeech, with columns for reject sites for all GPV sites
# 3. stats_speech.py -> AllSpeechThresholds.csv
# 4. match_gpv_tagging.py -> roc_GPV_audioset and gpv_tagging_results.npz
# 5. plot_finalèstats.py
# 6. reject_speech_tagging.py -> will rewrite the AcousticMeasurements files in a new folder, with columns for reject sites for all unseen sites

### Final files to be used in the AcousticMeasurements_renamed_withspeech folder

## Utility scripts that may be used 

# shufflewav.py
# listen_gpv.py

### unused scripts
## stats_gpv.py -> it is based on the rough method that find the threshold by matching the FPR
## stats_speech.py -> it is based on the rough method that find the threshold by matching the FPR