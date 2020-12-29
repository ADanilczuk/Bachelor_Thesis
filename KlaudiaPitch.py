import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from scipy import *
import scipy.fftpack
import math

import loadOnsetsFromFile as loff
import SaveDataInTxt as sd

gap = 1800
epsilon = 4000
sr = None


A4 = 440
C0 = A4*pow(2, -4.75)
noteName = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']    

def find_fund_freqs(input_signal, onsets): #liczymy fund_freqs dla kazdego fragmentu (onsetu)

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
            
            fund_freqs.append(fund_freq_for_window(fragment))


    return fund_freqs


def fund_freq_for_window(fragment): # liczymy hps (dla konkretnego fragmentu)

    fft = FFT(fragment)
    
    
    y = Y(fft, 4) # czy ta 4 ma sens...?
   # freqs = np.fft.fftfreq(len(y))
    freqs = np.fft.rfftfreq(len(fragment), 1 / sr)
    fund_freq = fundamental_frequency(y, freqs)
    return fund_freq


def FFT(input_signal): # liczymy fft
    return fft(input_signal)


def Y(input, M): # mnozymy ze soba wartosci wszystkich zdownsamplowanych tablic na odpowiednich indeksach
    downsampled = []
    N = len(input)
    end = 0
    result = []

    for m in range(0, M):
        downsampled.append(downsample(input, N, m+1))
        #rysuj_fft(downsampled[m])
        if m == M-1:
            end = len(downsampled[m])

    for i in range(0, end):
        result.append(1)
        for j in range(0, M):
            result[i] *= np.abs(downsampled[j][i]) # tutaj chcemy mnozyc amplitudy - czy abs jest prawidlowe?

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

            

   # freq = ind
    freq = freqs[ind]
    #freq = ind *  sr * 2 / len(y_array)
    #freq = 2 * math.pi * ind / len(y_array) # tutaj chcemy frequency zamiast indeksu. Czy to jest ok?
    # freq = ind / len(y_array) POWINNO BYC CHYBA ind * sample_rate / len(y_array), ale skad wziac sample_rate?!!
    # Moze sample rate to ten sr ktory dostalismy przy wczytywaniu nagrania z librosy...?
    return freq


def pitch2Note(freq):
    if (freq != 0 and freq != 0.0  ):
        h = round(12*log2(freq/C0))
        octave = h // 12
        n = h % 12
        return noteName[int(n)] + str(int(octave))
    else: return ""


def calculatePitchExtraction(name):
    song =  "C:/Alusia/Studia/Praca Dyplomowa/data/"+ name + ".wav"
    global sr
    input_signal, sr = librosa.load(song)
    
    onsets = loff.loadOnsetFromFile(name)
    # print("onsets", onsets)

    fundamentalFrequencies = find_fund_freqs(input_signal, onsets)
    time = np.arange(0, len(input_signal)) / sr

    noteSet = []
    for n in fundamentalFrequencies:
        noteSet.append(pitch2Note(n))
    # print("noteSet", noteSet)
    # sd.saveInTxt('freqs', name+'-K', fund_freqs, '\t')

    return (fundamentalFrequencies , noteSet)

if __name__ == "__main__":
    threshold = 5
    # name ="gdySlicznaPannaS2"
    name = "kotek2"
    song =  "C:/Alusia/Studia/Praca Dyplomowa/data/"+ name + ".wav"

    #window_size = 7800

    input_signal, sr = librosa.load(song)
    dlugosc = len(input_signal)
    print("input length:")
    print(len(input_signal))

    
    onsets = loff.loadOnsetFromFile(name)
    print("onsets", onsets)


    fund_freqs = find_fund_freqs(input_signal, onsets)

    time = np.arange(0, len(input_signal)) / sr

    noteSet = []
    for n in fund_freqs:
        noteSet.append(pitch2Note(n))
    print("noteSet", noteSet)
    sd.saveInTxt('freqs', name+'-K', fund_freqs, '\t')
    # for i in range(len(fund_freqs)):
    #     print("Fundamental frequency:")
    #     print(fund_freqs[i])
    #    # print("PITCH PERIOD:")
    #    # print(1/fund_freqs[i])


    fig, ax = plt.subplots()
   # ax.plot(time_first, first_window)
    ax.plot(time, input_signal)
    ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')

    # plt.show()