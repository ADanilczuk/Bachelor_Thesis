from matplotlib import pyplot as plt
from matplotlib import animation
from statistics import mean 
from matplotlib.collections import LineCollection
from pylab import rcParams

import math
import numpy as np
import librosa
import scipy.io.wavfile as scp

rcParams['figure.figsize'] = 10, 7

# mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/"
epsilon = 6000 

def approximateBySecondPolynomial(A,i, l):
    num = 0
    denom = 10
    j=-2
    if (i+j<0): j = (-1)*i
    while (i+j>=0 and i+j<l and j<= 2):
        num += (A[i+j][0]* j)
        j += 1
    return num/denom

def plot_onsets(input_signal, sr, onsets, windows, name):
    time = np.arange(0, len(input_signal)) / sr

    fig, ax = plt.subplots()
    minVal = min(input_signal)
    maxVal = max(input_signal)
    ax.plot(time, input_signal, zorder = 1)
    ax.set(xlabel='Czas [s]', ylabel='Amplituda')
    # ax.vlines(windows,  minVal, maxVal, lw=0.5, color='b', alpha=0.2, label = 'okna')
    ax.vlines(list(map(lambda x: x/sr, onsets)), minVal, maxVal, lw=0.75, color='black', alpha=0.8, label = 'początek dźwięku', zorder=2)
    ax.legend()
    sv = '../../grafiki/Testy/SurfMethod_' + name + '.png'
    plt.savefig(sv)
    plt.show()


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

def calculateOnsets(name, windowSize, threshold, version = 0):
    song =  mainPath +name +".wav"
    # sr- sample rate - how many samples is recorded per second
    inputSignal, sr = librosa.load(song)
    timeLength = len(inputSignal) / sr
    timeLine = np.linspace(0., timeLength, len(inputSignal))

    leftData = inputSignal
    signalLength = len(inputSignal)
   
    A = [[0 for x in range(2)] for y in range(math.ceil(signalLength/windowSize))] #A = [0] * math.ceil(leng/n_)
    lines = []
    # zaznacz kolejne okna na wykresie
    windowLines = []
    for c in range(math.ceil(signalLength/windowSize)):
        windowLines.append(c*windowSize*timeLength/signalLength)

    for i in range(math.ceil(signalLength/windowSize)-1):
        A[i][0] = 0
        for n in range(i*windowSize, (i+1)*windowSize) :
            if A[i][0] < leftData[n] :
                A[i][0] = leftData[n]
                A[i][1] = n

    onsetsNumbers1 = []
    onsetsNumbers = []
    for i in range(len(A)-1):
        d = approximateBySecondPolynomial(A,i,len(A))
        if d > threshold : 
            # onsetsNumbers1.append(A[i][1])
            onsetsNumbers.append(A[i][1])
            
    onsetsAfterElimination = pick_best_onset_in_epsilon(onsetsNumbers, epsilon)

    if (version != 0):
        # plot_onsets(inputSignal, sr, onsetsNumbers1, windowLines)
        plot_onsets(inputSignal, sr, onsetsAfterElimination, windowLines, name)
        # fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        # print(" time_", timeLine)
        # ax1.plot(timeLine, inputSignal)
        # ax1.set_xlabel("Czas [s]")
        # ax1.set_ylabel("Amplituda")
        # ax1.set_title('Sygnał wejściowy')

        # ax2.plot(timeLine, inputSignal)
        
        # ax2.set_xlabel("Czas [s]")
        # ax2.set_ylabel("Amplituda")
        # ax2.set_title('Sygnał wejściowy')
        # mx, mn = ax2.get_ylim()

        # ax2.vlines(windowLines, mx, mn, lw=0.5, color='b', alpha=0.4, label = 'okna')
        # ax2.vlines(onsetsTimes, mx, mn, lw=1, color='black', alpha=0.8, label = 'początek dźwięku')
        # ax2.legend()

    return onsetsNumbers

 
def showSong(name):
    onsets = calculateOnsets(name, 1)
    return onsets

if __name__ == "__main__": 

    windowSize = 600
    threshold = 0.0018
    name = 'KawalekPodlogiA'
    epsilon = 4000 
    onsets = calculateOnsets(name, windowSize, threshold, 1)

    plt.show()
