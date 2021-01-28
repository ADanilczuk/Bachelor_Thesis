import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from scipy import *
import scipy.fftpack
from math import log2, pow
import loadOnsetsFromFile as loff
import envelopeMatchFilter as enf

# mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/"

A4 = 440
C0 = 16.35 #A4*pow(2, -4.75)
noteName = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

gap = 1800
epsilon = 4000

def pitch2Note(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return noteName[n] + str(octave)

def find_fund_freqs(onsets, input_signal, sr): #liczymy fund_freqs dla kazdego fragmentu (onsetu)
    fund_freqs = []

    for i in range(0, len(onsets)):
            end = 0
            if i == len(onsets)-1:
                end = len(input_signal)
            else:
                end = onsets[i+1]
            fragment = []
            for j in range((int)(onsets[i]), (int)(end)):
                fragment.append(input_signal[j])
            fund_freqs.append(fund_freq_for_window(fragment, sr))
    return fund_freqs


def fund_freq_for_window(fragment, sr): # liczymy hps (dla konkretnego fragmentu)
    my_fft = fft(fragment)
    y = Y(my_fft, 4)
    freqs = np.fft.rfftfreq(len(fragment), 1 / sr)
    fund_freq = fundamental_frequency(y, freqs)
    return fund_freq


def Y(input, M): # mnozymy ze soba wartosci wszystkich zdownsamplowanych tablic na odpowiednich indeksach
    downsampled = []
    N = len(input)
    end = 0
    result = []
    for m in range(0, M):
        downsampled.append(downsample(input, N, m+1))
        if m == M-1:
            end = len(downsampled[m])

    for i in range(0, end):
        result.append(1)
        for j in range(0, M):
            result[i] *= np.abs(downsampled[j][i])

    return result


def downsample(input, length, n): # BIERZEMY CO n-TY ELEMENT Z TABLICY >INPUT<
    result = []
    for i in range(0, length, n):
        result.append(input[i])

    return result


def fundamental_frequency(y_array, freqs): # szukamy czestotliwosc o najwiekszej wartosci
    maksi = y_array[0]
    ind = 0
    for i in range(0, len(y_array)):
        if y_array[i] > maksi:
            maksi = y_array[i]
            ind = i

    freq = freqs[ind]
    return freq


def harmonic_product(onsets, input_signal, sr):
    fund_freqs = find_fund_freqs(onsets, input_signal, sr)
    return fund_freqs
    

def calculatePitchExtraction(name):
    song =  mainPath + name + ".wav"
    inputSignal, sr = librosa.load(song)

    onsets = loff.loadOnsetFromFile(name)
    fund_freqs = harmonic_product(onsets, inputSignal, sr)

    notes = []
    for f in fund_freqs:
        notes.append(pitch2Note(f))

    # print("Fundamental frequencies:")
    # print(fund_freqs)
    # print("Notes:")
    # print(notes)

    return (fund_freqs, notes)

if __name__ == "__main__":

    query_name = "KawalekPodlogiA"
    calculatePitchExtraction(query_name)