import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display


def ACF(n, input_signal):

    #funkcja ACF 

    N = len(input_signal)
    result = 0

    for i in range(0, N-n):
        result += input_signal[i] * input_signal[i+n]

    result *= 1/(N-n)
    return result

def value_that_maximizes_ACF(input_signal):

    #znajdz wartosc dla ktorej ACF jest najwiekszy 

    result = 0
    N = len(input_signal)

    for i in range(0, N):
        val = ACF(i, input_signal)
        if val > result:
            result = val

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
        
        print("FRAGMENT LENGTH")
        print(len(fragment))

        pitch_periods.append(value_that_maximizes_ACF(fragment))
    
    return pitch_periods

def autocorrelation_function(onsets, query_name):
    threshold = 5
    song =  "/Users/klaudiuszek/Desktop/Licencjat/Data/" + query_name + ".wav"

    input_signal, sr = librosa.load(song)
    print("input length:")
    print(len(input_signal))

    #time = np.arange(0, len(input_signal)) / sr

    pitch_periods = find_pitch_periods(input_signal, onsets)
    '''
    print("PITCH PERIODS:")
    
    for i in range(len(pitch_periods)):
        print(pitch_periods[i])
    '''

    return pitch_periods

if __name__ == "__main__":

    onsets = [7482, 18927, 30646, 41546, 52174, 63620, 78881, 90872, 100682]
    query_name = "wlazlKotekNucenie5s"

    pitch_periods = autocorrelation_function(onsets, query_name)
