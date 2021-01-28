from __future__ import division
from matplotlib import pyplot as plt
from matplotlib import animation
from statistics import mean 
from matplotlib.collections import LineCollection
from scipy.fftpack import fft
from scipy import signal
import librosa


import loadOnsetsFromFile as loff
import envelopeMatchFilter as enf
import SaveDataInTxt as sd

import math
import numpy as np
import librosa as lba
import scipy.io.wavfile as scp
import scipy.signal as scps
from math import log2, pow

# mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/"

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
    
def printCepstralAnalysis(data, sr,frequencyVector, quefrencyVector, ceps):
    timeLength = len(data) / sr
    timeLine = np.linspace(0., timeLength, len(data))

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    print(" time_", timeLine)
    ax1.plot(timeLine, data)
    ax1.set_xlabel("Czas [s]")
    ax1.set_ylabel("Amplituda")
    ax1.set_title('Sygnał wejściowy pojedynczego dźwięku')

    ax2.plot(frequencyVector, np.fft.rfft(data)) 
    ax2.set_xlabel("Częstotliwość (Hz)")
    ax2.set_ylabel("Moc")
    ax2.set_title('Spektrum FFT') 
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)


    ax3.plot(quefrencyVector,ceps) 
    ax3.set_xlabel("Quefrency (s)")
    ax3.set_ylabel("Amplituda")
    ax3.set_title('Cepstrum')


def calculatePitchExtraction(name, version = 1):
    
    threshold = 5
    song =  mainPath + name +".wav"

    # sr- sample rate - how many samples is recorded per second
    input_signal, sr = librosa.load(song)
    window_size = 7800

    onsets = loff.loadOnsetFromFile(name)
    if onsets == '' :  
        # print("no onsets")
        onsets = enf.get_onsets_locations(input_signal, window_size, threshold)
        onsets = enf.pick_best_onset_in_epsilon(onsets, 4000)
    time = np.arange(0, len(input_signal)) / sr
    leftData = input_signal 
    
    onsetAmount = len(onsets)
    # onsets = onsets[np.argsort(onsets[:,0])]
    i = 0
    l = 0
    fundamentalFrequencies = []
    fundamentalFrequencies2 = []

    fmax = 600 #Hz
    fmin = 200  #Hz

    while (i<onsetAmount):
        if i == onsetAmount-1: end = len(leftData)
        else: end = onsets[i+1]-1
        partialData = leftData[onsets[i] : end]
        
        logFft = np.log(np.abs(np.fft.rfft(partialData)))
        cepstrum = np.fft.rfft(logFft)

        frequencyVector = np.fft.rfftfreq(len(partialData), d=1/sr)
        df = frequencyVector[1] - frequencyVector[0]
        # df is a sample spacing that appeared in the frequencyVector
        quefrencyVector = np.fft.rfftfreq(logFft.size, df)

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
        
        valid = (quefrencyVector > 1/fmax) & (quefrencyVector <= 1/fmin)
        # Maximal value among all cepstrum data
        maxQuefrencyIndex = np.argmax(np.abs(cepstrum)[valid])
        f0 = 1/quefrencyVector[valid][maxQuefrencyIndex]
        fundamentalFrequencies.append(f0)

        # Maximal value among peaks in cepstrum data
        (maxIndx , maxVal)=findMaxIndex(peaks[valid])
        f02 = 1/quefrencyVector[valid][maxIndx]
        fundamentalFrequencies2.append(f02)
        
        # printCepstralAnalysis(partialData, sr,frequencyVector, quefrencyVector, ceps)

        i += 1
    
    # print("Fundamental Frequencies", fundamentalFrequencies)
    # print("Fundamental Frequencies2", fundamentalFrequencies2)
    noteSet = []
    for n in fundamentalFrequencies:
        noteSet.append(pitch2Note(n))
    noteSet2 = []
    for n in fundamentalFrequencies2:
        noteSet2.append(pitch2Note(n))


    if version == 1 : return (fundamentalFrequencies , noteSet)
    if version == 2 : return (fundamentalFrequencies2 , noteSet2)
    

if __name__ == "__main__": 
    (freqs, notes) = calculatePitchExtraction("kotek1", 2)
    print("Fundamental Frequencies", freqs)
    print("noteSet", notes)
    plt.show()