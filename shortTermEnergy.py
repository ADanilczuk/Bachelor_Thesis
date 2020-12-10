import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

gap = 1800
epsilon = 4000

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

if __name__ == "__main__":
    threshold = 0.2
    # song directory
    song =  "song.wav"

    input_signal, sr = librosa.load(song)
    print(len(input_signal))

    window_size = 15000

    energies = compute_energies(input_signal, window_size)

    onsets = get_onsets_locations(threshold, energies, window_size)

    time = np.arange(0, len(input_signal)) / sr

    print(window_size)
    print("onsety:")
    print(len(onsets))
    for i in range(0, len(onsets)):
        print(onsets[i])
        onsets[i] = onsets[i] / sr

    fig, ax = plt.subplots()

    for xc in onsets:
        plt.axvline(x=xc, color='k')

    ax.plot(time, input_signal)
    ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')

    plt.show()





