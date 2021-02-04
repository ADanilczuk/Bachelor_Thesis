from __future__ import division
from matplotlib import pyplot as plt
from matplotlib import animation
from statistics import mean 
from matplotlib.collections import LineCollection
from scipy.fftpack import fft
import librosa

import loadOnsetsFromFile as loff
import envelopeMatchFilter as enf
import saveDataInTxt as sd

import math
import numpy as np
import librosa as lba
import scipy.io.wavfile as scp
import scipy.signal as scps
from math import log2, pow

A4 = 440
C0 = A4*pow(2, -4.75)
noteName = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
# mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/"

def pitch2Note(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return noteName[n] + str(octave)

def findMinIndex(fData):
    indx = [0,0,0]
    for j in range(1,len(fData)):
        m = np.argmin([fData[indx[0]],fData[indx[1]],fData[indx[2]]])
        if fData[indx[m]] < fData[j]:
            indx[m] = j
    i = np.argmin([fData[indx[0]],fData[indx[1]],fData[indx[2]]])
    return indx[i]
        

def calculatePitchExtraction(name):
    
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
    
    f1 = plt.figure(1)
    # fig, ax = plt.subplots()
    plt.plot(time, input_signal)
    
    onsetAmount = len(onsets)
    # onsets = onsets[np.argsort(onsets[:,0])]
    i = 0
    l = 0
    fundamentalFrequencies = []
    f2 = plt.figure(2)
    while (i<onsetAmount):
        if i == onsetAmount-1: end = len(leftData)
        else: end = onsets[i+1]-1
       
        y = np.fft.rfft(leftData[onsets[i] : end])
        z = np.fft.rfftfreq(len(leftData[onsets[i] : end]), 1 / sr)

        k = findMinIndex(y)
        frequency = z[k]
        
        fundamentalFrequencies.append(frequency)
        plt.plot( list(range(len(y))),np.abs(y))
        
        i += 1
    
    noteSet = []
    for n in fundamentalFrequencies:
        noteSet.append(pitch2Note(n))
    
    # sd.saveInTxt('notes', name, noteSet, '\t')
    return (fundamentalFrequencies , noteSet)

if __name__ == "__main__": 
    # calculatePitchExtraction('nucenie2')
    (propsedFreqs, proposedNotes) = calculatePitchExtraction("kotek1")
    print("Fundamental Frequencies", propsedFreqs)
    print("noteSet", proposedNotes)
    # calculatePitchExtraction("gdySlicznaPannaS2")
    # calculatePitchExtraction("aaa1")
    # calculatePitchExtraction("piano1")
    # plt.show()
