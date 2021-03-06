import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from pylab import rcParams

f = [3, 3, 4, 4, -1, -1, -2, -2, -2, -2, -2, -2]
gap = 2500
epsilon = 4000

rcParams['figure.figsize'] = 10, 4
# mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/"

def A_k(input_signal, window_size, k):
    result = 0

    start = k * gap
    end = k * gap + window_size
    for i in range(start, end):
        if input_signal[i] > result:
            result = input_signal[i]

    return result

def B_k(input_signal, window_size, k):
    a_k = A_k(input_signal, window_size, k)
    result = (a_k / (0.2 + 0.1 * a_k)) ** 0.7

    return result

def C_k(input_signal, window_size, k):
    #liczymy konwolucje
    result = 0
    for i in range(0, 12):
        result += B_k(input_signal,window_size,k-i) * f[i]

    return result

def get_onsets_locations(input_signal, window_size, threshold):
    onsets = []
    k = 0
    while k * gap + window_size < len(input_signal):
        c_k = C_k(input_signal, window_size, k)

        if c_k > threshold:
            onsets.append(k * gap)
        k += 1

    return onsets

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

def plot_onsets(input_signal, sr, onsets, fileName):
    time = np.arange(0, len(input_signal)) / sr
    #print("onsety:")
    
    print(len(onsets))
    for i in range(0, len(onsets)):
        # print(onsets[i])
        onsets[i] = onsets[i] / sr
    #  print(onsets[i])
    
    fig, ax = plt.subplots()
    minVal = min(input_signal)
    maxVal = max(input_signal)
    ax.plot(time, input_signal, zorder = 1)
    ax.set(xlabel='Czas [s]', ylabel='Amplituda')
    ax.vlines(onsets, minVal, maxVal, lw=0.75, color='black', alpha=0.8, label = 'początek dźwięku', zorder=2)
    ax.legend()
    if fileName!='':
        plt.savefig('../../grafiki/Onsets/'+fileName+'.png')
    
    plt.show()

def envelope_match_filter(query_name, threshold, window_size):
    # directory to the query
    song =  mainPath + query_name + ".wav"

    input_signal, sr = librosa.load(song)

    onsets = get_onsets_locations(input_signal, window_size, threshold)

    # onsets = pick_best_onset_in_epsilon(onsets, epsilon)

    fileName = 'EnvelopeMatchFilter_' + query_name + '_' + str(window_size) + '_' + str(threshold) #+ '_' + str(epsilon)
    plot_onsets(input_signal, sr, onsets, fileName)

    return onsets


if __name__ == "__main__":
    query_name = "WlazlKotekK"
    threshold = 0.8
    window_size = 2900
    # epsilon = 8000
    onsets = envelope_match_filter(query_name, threshold, window_size)