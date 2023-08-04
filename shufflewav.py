import librosa
import numpy as np
import soundfile

def shufflewav(filepath,savepath,seg=0.2):
    wav,sr = librosa.load(filepath,sr=None,mono=False)
    len = int(np.floor(seg*sr))
    totallen = wav.shape[0]
    nseg = int(totallen / len)
    wav = wav[:nseg*len]
    
    wav = wav.reshape(nseg,len)
    #shuffle first dimension of wav
    indord = np.random.permutation(nseg)

    wav= wav[indord].reshape(-1)
    soundfile.write(savepath,wav,samplerate=sr)




shufflewav('Shortest/test.wav','test_reord.wav',seg = 0.122)