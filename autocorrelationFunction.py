import librosa
import matplotlib.pyplot as plt
from math import log2, pow
import loadOnsetsFromFile as loff
import EnvelopeMatchFilter as enf
import math
import numpy as np
import scipy.io.wavfile as scp

A4 = 440
C0 = 16.35 #A4*pow(2, -4.75)
noteName = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    

def pitch2Note(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return noteName[n] + str(octave)

def ACF(n, input_signal):
    #funkcja ACF 

    N = len(input_signal)
    result = 0
    
    for i in range(0, int(N-n)):
        result += input_signal[i] * input_signal[i+n]

    result *= 1/(N-n)
    return result

def value_that_maximizes_ACF(input_signal):
    #znajdz wartosc dla ktorej ACF jest najwiekszy 

    result = 0
    max_val = 0.0
    N = len(input_signal)

    for i in range(22, 111):
        val = ACF(i, input_signal)
        if val > max_val:
            max_val = val
            result = i

    return result

def find_pitch_periods(input_signal, onsets):
    #znajdz pitch periods dla kazdego fragmentu od onsetu do onsetu 

    pitch_periods = []
    
    for i in range(0, len(onsets)):
        end = 0
        if i == len(onsets)-1:
            end = len(input_signal)
        else:
            end = onsets[i+1]
        
        fragment = []

        for j in range((int)(onsets[i]), (int)(end)):
            fragment.append(input_signal[j])
        
        pitch_periods.append(value_that_maximizes_ACF(fragment))
    
    return pitch_periods

def autocorrelation_function(onsets, input_signal, sr):

    pitch_periods = find_pitch_periods(input_signal, onsets)

    fund_freqs = []
    for i in range(len(pitch_periods)):
        fund_freqs.append(sr/pitch_periods[i])
    
    return fund_freqs


def calculatePitchExtraction(name):
    mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
    #mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/"
    song =  mainPath + query_name + ".wav"
    inputSignal, sr = librosa.load(song)

    onsets = loff.loadOnsetFromFile(name)

    fund_freqs = autocorrelation_function(onsets, inputSignal, sr)

    notes = []
    for f in fund_freqs:
        notes.append(pitch2Note(f))
    print("Fundamental frequencies:")
    print(fund_freqs)
    print("Notes:")
    print(notes)

    return (fund_freqs, notes);

if __name__ == "__main__":
    
    query_name = "GdySlicznaPannaK"
    calculatePitchExtraction(query_name)
    
