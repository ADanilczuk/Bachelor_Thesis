from __future__ import division
from matplotlib import pyplot as plt
from matplotlib import animation
from statistics import mean 
from matplotlib.collections import LineCollection
from scipy.fftpack import fft
from scipy import signal
import librosa


import loadOnsetsFromFile as loff
import EnvelopeMatchFilter as enf
import SaveDataInTxt as sd

import math
import numpy as np
import librosa as lba
import scipy.io.wavfile as scp
import scipy.signal as scps
from math import log2, pow

A4 = 440
C0 = A4*pow(2, -4.75)
noteName = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    

def pitch2Note(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return noteName[n] + str(octave)

def findMaxIndex(fData):
    maxIndx = 0
    maxVal = fData[0]
    for j in range(1,len(fData)):
        if maxVal < fData[j]:
            maxIndx = j
            maxVal = fData[j]
    return (maxIndx , maxVal)
    

def calculatePitchExtraction(name, version = 1):
    
    threshold = 5
    song =  "C:/Alusia/Studia/Praca Dyplomowa/data/"+name +".wav"

    # sr- sample rate - how many samples is recorded per second
    input_signal, sr = librosa.load(song)
    window_size = 7800

    onsets = loff.loadOnsetFromFile(name)
    if onsets == '' :  
        print("no onsets")
        onsets = enf.get_onsets_locations(input_signal, window_size, threshold)
        onsets = enf.pick_best_onset_in_epsilon(onsets, 4000)
    time = np.arange(0, len(input_signal)) / sr
    leftData = input_signal 
    
    f1 = plt.figure(1)
    # fig, ax = plt.subplots()
    plt.plot(time, input_signal)
    
    onsetAmount = len(onsets)
    # onsets = onsets[np.argsort(onsets[:,0])]
    i = 0
    l = 0
    fundamentalFrequencies = []
    fundamentalFrequencies2 = []
    f2 = plt.figure(2)

    fmax = 600 #Hz
    fmin = 200  #Hz

    while (i<onsetAmount):
        if i == onsetAmount-1: end = len(leftData)
        else: end = onsets[i+1]-1
        partialData = leftData[onsets[i] : end]
  
        frequencyVector = np.fft.rfftfreq(len(partialData), d=1/sr)
        logFft = np.log(np.abs(np.fft.rfft(partialData)))
        cepstrum = np.fft.rfft(logFft)
        df = frequencyVector[1] - frequencyVector[0]
        quefrency_vector = np.fft.rfftfreq(logFft.size, df)

        ceps = cepstrum 
                
        nceps=len(ceps)
        peaks = np.zeros(nceps)
        k = 3
        while(k < nceps - 2):
            # print("k",k)
            y1 = ceps[k - 1]
            y2 = ceps[k]
            y3 = ceps[k + 1]
            if (y2 > y1 and y2 >= y3):
                peaks[k]=ceps[k]
            k=k+1
        
        valid = (quefrency_vector > 1/fmax) & (quefrency_vector <= 1/fmin)
        # Maximal value among all cepstrum data
        maxQuefrencyIndex = np.argmax(np.abs(cepstrum)[valid])
        f0 = 1/quefrency_vector[valid][maxQuefrencyIndex]
        fundamentalFrequencies.append(f0)

        # Maximal value amond peaks in cepstrum data
        (maxIndx , maxVal)=findMaxIndex(peaks[valid])
        f02 = 1/quefrency_vector[valid][maxIndx]
        fundamentalFrequencies2.append(f02)
        
        i += 1
    
    # print("Fundamental Frequencies", fundamentalFrequencies)
    # print("Fundamental Frequencies2", fundamentalFrequencies2)
    noteSet = []
    for n in fundamentalFrequencies:
        noteSet.append(pitch2Note(n))
    noteSet2 = []
    for n in fundamentalFrequencies2:
        noteSet2.append(pitch2Note(n))

    # sd.saveInTxt('freqs', name+'-A', fundamentalFrequencies, '\t')
    if version == 1 : return (fundamentalFrequencies , noteSet)
    if version == 2 : return (fundamentalFrequencies2 , noteSet2)

if __name__ == "__main__": 
    # calculatePitchExtraction('nucenie2')
    # calculatePitchExtraction("piano3")
    # calculatePitchExtraction("gdySlicznaPannaS2")
    (freqs, notes) = calculatePitchExtraction("piano3", 1)
    print("Fundamental Frequencies", freqs)
    print("noteSet", notes)
    # calculatePitchExtraction("aaa1")
    plt.show()
    # calculatePitchExtraction("piano1")
    # plt.show()`
