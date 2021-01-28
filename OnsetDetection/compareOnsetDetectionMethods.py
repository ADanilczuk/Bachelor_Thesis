import time
from collections import Counter
from matplotlib import pyplot as plt
from math import log2, pow
import re 
import numpy as np



def mesureTimeAndExecute(function, *args):
    tic = time.perf_counter()
    onsets = function(*args)
    toc = time.perf_counter()
    t = toc - tic
     
    return  (t, onsets)

def plot_onsets(input_signal, sr, onsets, windows = []):
    time = np.arange(0, len(input_signal)) / sr

    for i in range(0, len(onsets)):
        print(onsets[i])
        onsets[i] = onsets[i] / sr

    fig, ax = plt.subplots()
    minVal = min(input_signal)
    maxVal = max(input_signal)
    ax.plot(time, input_signal, zorder = 1)
    ax.set(xlabel='Czas [s]', ylabel='Amplituda')
    if (len(windows) >0):
        ax.vlines(windows, minVal, maxVal, lw=0.5, color='b', alpha=0.1, label = 'okna')
    ax.vlines(onsets, minVal, maxVal, lw=0.75, color='black', alpha=0.8, label = 'początek dźwięku', zorder=2)
    ax.legend()
    # plt.savefig('ShortTermEnergy_kotekSzum_5450_5.png')
    plt.show()


def compareOnsetDetecion(name, version):
    
    # (t1, (propsedFreqs, proposedNotes)) = mesureTimeAndExecute(ProposedMethod.calculatePitchExtraction, name)
    # (t2, (KlaudiaFreqs, KlaudiaNotes)) = mesureTimeAndExecute(KlaudiaPitch.calculatePitchExtraction, name)
    # (t3, (CepstralFreqs, CepstralNotes)) = mesureTimeAndExecute(tryCepstralMethod.calculatePitchExtraction, name, 1)
    # (t4, (CepstralFreqs2, CepstralNotes2)) =  mesureTimeAndExecute(tryCepstralMethod.calculatePitchExtraction, name, 2)

    if version == 1:
        print("times", t1, t2, t3, t4)
        print("propsedFreqs", propsedFreqs)
        print("KlaudiaFreqs", KlaudiaFreqs)
        print("CepstralFreqs", CepstralFreqs)
        print("CepstralFreqs2", CepstralFreqs2)
        print("")
    
        print("proposedNotes", proposedNotes)
        print("KlaudiaNotes", KlaudiaNotes)
        print("CepstralNotes", CepstralNotes)
        print("CepstralNotes2", CepstralNotes2)

    


if __name__ == "__main__": 
    name = "gdySlicznaPannaH2"
   
    (freqs, notes) = chooseNotes(name)
    print("freqs", freqs)
    print("notes", notes)
    # print(chooseNotes(name))

  
    
    
   
   
    
    
