import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from scipy import *
import scipy.fftpack
import math

gap = 1800
epsilon = 4000

def find_fund_freqs(input_signal, onsets, sr): #liczymy fund_freqs dla kazdego fragmentu (onsetu)

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

    fft = FFT(fragment)
    y = Y(fft, 4)
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

    freq = freqs[ind]

    return freq


def harmonic_product(onsets, query_name):
    threshold = 5
    song =  "/Users/klaudiuszek/Desktop/Licencjat/Data/" + query_name + ".wav"

    input_signal, sr = librosa.load(song)
    #dlugosc = len(input_signal)

    fund_freqs = find_fund_freqs(input_signal, onsets, sr)

    return fund_freqs
    #time = np.arange(0, len(input_signal)) / sr
    ''' 
    for i in range(len(fund_freqs)):
        print("Fundamental frequency:")
        print(fund_freqs[i])
        print("PITCH PERIOD:")
        print(1/fund_freqs[i])
    '''

if __name__ == "__main__":

    onsets = [7482, 18927, 30646, 41546, 52174, 63620, 78881, 90872, 100682]
    query_name = "wlazlKotekNucenie5s"

    fund_freqs = harmonic_product(onsets, query_name)

    #print(fund_freqs)
    