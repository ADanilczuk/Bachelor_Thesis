import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from scipy import *
import scipy.fftpack
import math
import mido


def freqs_2_MIDI(freqs):

    midi = []
    for freq in freqs:
        m = 69 + 12 * np.log2(freq/440)
        midi.append(int(m))

    return midi


def match_score(q, t):
    if q == t: 
        return 2
    else:
        return -2


def compute_align_score(inputMIDI, targetMIDI):
    alignScore = []

    for i in range(len(inputMIDI)):
        alignScore.append([])

        for j in range(len(targetMIDI)):
            
            alignScore[i].append(0)
            if i > 0:
                alignScore[i][j] = max(alignScore[i][j], alignScore[i-1][j])
            if j > 0:
                alignScore[i][j] = max(alignScore[i][j], alignScore[i][j-1])
            if i > 0 and j > 0:
                alignScore[i][j] = max(alignScore[i][j], match_score(inputMIDI[i], targetMIDI[j]) + alignScore[i-1][j-1])
        
    return alignScore[len(inputMIDI)-1][len(targetMIDI)-1]


def dynamic_programming(fundamental_freqs_query, target_song_name):
    queryMIDI = freqs_2_MIDI(fundamental_freqs_query)
    directory = "/Users/klaudiuszek/Desktop/Licencjat/Data/" + target_song_name + ".midi"
    target = mido.MidiFile(directory, clip=True)
    targetMIDI = []
    
    """
     printing MIDI
     
    print(targetMIDI)
    for m in queryMIDI:
        print(m)
    """
    for msg in target.tracks[0]:
        if not msg.is_meta:
            if msg.type == 'note_on':
                #print(msg.note)
                targetMIDI.append(msg.note)

    score = compute_align_score(queryMIDI, targetMIDI)

    print(score)


if __name__ == "__main__":
    song =  "/Users/klaudiuszek/Desktop/Licencjat/Data/nucenie.wav"
    fundamental_freqs_input = [373.95120499851237, 312.97536154258165, 314.91564759439433, 335.51088065283915, 277.42922723794953, 275.5521026183549, 246.0278496831206, 304.00218210672483, 375.21935655410795]
    dynamic_programming(fundamental_freqs_input, "wlazlKotek5s")

    

