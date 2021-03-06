from __future__ import division
from matplotlib import pyplot as plt
from matplotlib import animation
from statistics import mean 
from matplotlib.collections import LineCollection
from math import log2, pow

import loadOnsetsFromFile as loff
import envelopeMatchFilter as enf
import math
import numpy as np
import librosa 
import scipy.io.wavfile as scp

# mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/"

A4 = 440
C0 = 16.35 #A4*pow(2, -4.75)
noteName = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    

def pitch2Note(freq):
    print(freq)
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return noteName[n] + str(octave)


def AMDF(n,N,A):
    result = 0
    partResult = 0
    k=0
    while (k<=N/2): #-1-n):
        partResult += math.fabs(A[k]-A[k+n])
        k += 1
    return partResult/(N-n)

    
def calculatePitchExtraction(name):
    song =  mainPath + name +".wav"
    # sr- sample rate - how many samples is recorded per second
    inputSignal, sr = librosa.load(song)
    time = np.arange(0, len(inputSignal)) / sr

    fmax = 1000 #Hz below C6 note
    fmin = 200 #Hz above G3 note
    elementWithMinPeriod = round(sr/fmax)
    elementWithMaxPeriod = round(sr/fmin)
    # print("timeMax", elementWithMinPeriod, elementWithMaxPeriod)

    A = []
    fundamentalFrequencies = []
    onsets = loff.loadOnsetFromFile(name)
    if onsets == '' :  
        onsets = enf.get_onsets_locations(inputSignal, window_size= 400, threshold = 5)
        onsets = enf.pick_best_onset_in_epsilon(onsets, 4000)

    onsetAmount = len(onsets)
    i = 0
    l = 0
    
    # print(onsetAmount)
    while (i<onsetAmount):
        if i == onsetAmount-1: end = len(inputSignal)
        else: end = onsets[i+1]-1
        y = inputSignal[onsets[i] : end]

        smallestIndex = 0
        smallest = 0.003
        j = elementWithMinPeriod
        while j < elementWithMaxPeriod: 
            AMDFvalue =  AMDF(j,len(y),y)
            if (j==elementWithMinPeriod): smallest = AMDFvalue
            if (AMDFvalue < smallest) :
                smallest = AMDFvalue
                smallestIndex = j
            j += 1
        pitchPeriod = smallestIndex/sr
        if pitchPeriod == 0: fundamentalFrequencies.append(0)
        else: fundamentalFrequencies.append(1/pitchPeriod)
        # print("A.append(smallestOffset)", smallestIndex, pitchPeriod)
        i += 1

    # print("fundamentalFrequencies", fundamentalFrequencies)

    noteSet = []
    for n in fundamentalFrequencies:
        noteSet.append(pitch2Note(n))
    
    # sd.saveInTxt('notes', name, noteSet, '\t')
    return (fundamentalFrequencies , noteSet)

if __name__ == "__main__":
    (fundamentalFrequencies , noteSet) = calculatePitchExtraction('KawalekPodlogiK')
    print("Freqs", fundamentalFrequencies)
    notes = []
    for f in fundamentalFrequencies:
        notes.append(pitch2Note(f))
    # print(notes)

