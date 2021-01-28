from matplotlib import pyplot as plt
from matplotlib import animation
from statistics import mean 
from matplotlib.collections import LineCollection
from pylab import rcParams

import math
import numpy as np
import librosa 
import scipy.io.wavfile as scp

import compareOnsetDetectionMethods as cod
from scipy import signal

# mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/"
epsilon = 6000

rcParams['figure.figsize'] = 10, 7

def lowpassChebychevsFilter(partialData, sr, version = 0):
    # Chebyshev Type II filter 
    # Only frequencies lower than 1396.91Hz (which is F6) can are left
    sos = signal.cheby2(12, 20, 1396.91, 'low', fs=sr, output='sos')
    reultData = signal.sosfilt(sos, partialData)

    if (version != 0):
        t = np.linspace(0., len(partialData)/sr, len(partialData))
        
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(t, partialData)
        ax1.set_title('Sygnał wejściowy')

        ax2.plot(t, reultData)
        ax2.set_title('Po zastosowaniu filtra dolnoprzepustowego od częstotliwości 1396.91Hz')
        ax2.set_xlabel('Czas [sekundy]')

        plt.show()

    return reultData

def pick_best_onset_in_epsilon(onsets, epsilon):
    n = len(onsets)
    result = []
    to_delete = set()
    for i in range(0, n):
        for j in range(0, n):
            if abs(onsets[i] - onsets[j])  > epsilon or i == j:
                continue
            if(onsets[i] > onsets[j]):
                to_delete.add(i)
            else:
                to_delete.add(j)

    for i in range(0, n):
        if i not in to_delete:
            result.append(onsets[i])
        
    return result

def plot_onsets(inputSignal, sr, onsets, windows = [], lowpassedData = []):
    time = np.arange(0, len(inputSignal)) / sr

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    print(" time_", time)
    ax1.plot(time, inputSignal)
    ax1.set_xlabel("Czas [s]")
    ax1.set_ylabel("Amplituda")
    ax1.set_title('Sygnał wejściowy')

    ax2.plot(time, lowpassedData)

    ax2.set_xlabel("Czas [s]")
    ax2.set_ylabel("Amplituda")
    ax2.set_title('Po zastosowaniu filtra dolnoprzepustowego od częstotliwości 1396.91Hz')
    mx, mn = ax2.get_ylim()

    ax2.vlines(windows, mx, mn, lw=0.5, color='b', alpha=0.1, label = 'okna')
    ax2.vlines(list(map(lambda x: x/sr, onsets)), mx, mn, lw=0.75, color='black', alpha=0.8, label = 'początek dźwięku')
    ax2.legend()
    # plt.savefig('../../grafiki/LinearScaling_gdySlicznaPannaS_plots.png')
    plt.show()


def calculateOnsets(name, windowSize, treshold, version = 0):
    song =  mainPath +name +".wav"

    # sr- sample rate - how many samples is recorded per second
    inputSignal, sr = librosa.load(song)
    timeLength = len(inputSignal) / sr
    timeLine = np.linspace(0., timeLength, len(inputSignal))

    lowpassedData = lowpassChebychevsFilter(inputSignal, sr, 0)
    
    signalLength = len(inputSignal)
    
    # 𝐴𝑘 = max(𝐿𝑃𝐹{𝑥[𝑛]}|𝑘𝑛0 ≤ 𝑛 ≤ (𝑘 + 1)𝑛0)
    A = [[0 for x in range(2)] for y in range(math.ceil(signalLength/windowSize))]
    windowLines = []
    for c in range(math.ceil(signalLength/windowSize)):
        windowLines.append(c*windowSize*timeLength/signalLength)
   
    for i in range(math.ceil(signalLength/windowSize)-1):
        A[i][0] = 0
        for n in range(i*windowSize, (i+1)*windowSize) :
            if A[i][0] < lowpassedData[n] :
                A[i][0] = lowpassedData[n]
                A[i][1] = n
    d = 0
    onsetsNumbers = []
    for i in range(1, len(A)-1):
        d = A[i][0] - A[i-1][0] 
        if d > threshold : 
            onsetsNumbers.append(A[i][1])
            
    onsetsAfterElimination = pick_best_onset_in_epsilon(onsetsNumbers, epsilon)
   
    if (version != 0):
        plot_onsets(inputSignal, sr, onsetsAfterElimination, windowLines, lowpassedData)
        
    return onsetsAfterElimination

 
def showSong(name):
    onsets = calculateOnsets(name, 1)
    return onsets

if __name__ == "__main__": 
    # onsets = showSong('wlazlKotekNucenie5sGlosne')'

    windowSize = 1000
    threshold = 0.01
    name = 'SzlaDzieweczkaA'
    # epsilon = 4500
    onsets = calculateOnsets(name, windowSize, threshold, 1)
    plt.show()