import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from pylab import rcParams

epsilon = 6000
rcParams['figure.figsize'] = 10, 4
# mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/"
epsilon = 6000

def kth_energy(k, input_signal, window_size):
    start = (k * window_size)
    if start < 0:
        start = 0
    
    end = (k + 1) * window_size
    if end > len(input_signal):
        end = len(input_signal)
    
    if end < start or end < 0:
        return 0
    
    result = 0
    for i in range(start, end):
        result += input_signal[i] * input_signal[i]
    
    return result

def compute_energies(input_signal, window_size):
    k = 0
    energies = []
    while (k+1)*window_size - 1 < len(input_signal):
        energies.append(kth_energy(k, input_signal, window_size))
        k += 1
    
    return energies

def get_onsets_locations(threshold, energies, window_size):
    onsets = []
    for i in range(1, len(energies)):
        d_i = energies[i] - energies[i-1]
        if d_i > threshold:
            onsets.append(i * window_size)

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

def plot_onsets(input_signal, sr, onsets, fileName = ''):
    time = np.arange(0, len(input_signal)) / sr
    
    for i in range(0, len(onsets)):
        print(onsets[i])
        onsets[i] = onsets[i] / sr
    
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



def short_term_energy(query_name, threshold, window_size):

    song =  mainPath + query_name + ".wav"

    input_signal, sr = librosa.load(song)
    print(len(input_signal))

    
   
    energies = compute_energies(input_signal, window_size)

    onsets = get_onsets_locations(threshold, energies, window_size)
    
    #onsets = pick_best_onset_in_epsilon(onsets, epsilon)

    fileName = 'ShortTerm_' + query_name + '_' + str(window_size) + '_' + str(threshold) #+ '_' + str(epsilon)
    plot_onsets(input_signal, sr, onsets, fileName)

    return onsets

if __name__ == "__main__":
    query_name = "WlazlKotekK"
    threshold = 5
    window_size = 5450
    # epsilon = 8000
    onsets = short_term_energy(query_name, threshold, window_size)