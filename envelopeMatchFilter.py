import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

f = [3, 3, 4, 4, -1, -1, -2, -2, -2, -2, -2, -2]
gap = 1800
epsilon = 4000

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
            print(c_k)
            onsets.append([k * gap, c_k])
        k += 1

    return onsets

def pick_best_onset_in_epsilon(onsets, epsilon):
    n = len(onsets)
    result = []
    to_delete = set()
    for i in range(0, n):
        for j in range(0, n):
            if abs(onsets[i][0] - onsets[j][0])  > epsilon or i == j:
                continue
            if(onsets[i][1] <= onsets[j][1]):
                to_delete.add(i)
            else:
                to_delete.add(j)

    for i in range(0, n):
        if i not in to_delete:
            result.append(onsets[i][0])

    return result

if __name__ == "__main__":
    threshold = 5
    # song directory
    song =  "song.wav"

    input_signal, sr = librosa.load(song)

    window_size = 7800

    onsets = get_onsets_locations(input_signal, window_size, threshold)

    time = np.arange(0, len(input_signal)) / sr

    onsets = pick_best_onset_in_epsilon(onsets, epsilon)



    print("onsety:")
    print(len(onsets))
    for i in range(0, len(onsets)):
        print(onsets[i])
        onsets[i] = onsets[i] / sr
        print(onsets[i])


    fig, ax = plt.subplots()

    for xc in onsets:
        plt.axvline(x=xc, color='k')

    ax.plot(time, input_signal)
    ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')

    plt.show()
