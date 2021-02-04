import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import scipy.fftpack
import math
import mido
from copy import deepcopy
import datetime


def freqs_2_MIDI(freqs):

    midi = []
    for freq in freqs:
        m = 69 + 12 * np.log2(freq/440)
        midi.append(int(m))

    return midi


def match_score(q, bucket):

    if q >= bucket - 2 and q <= bucket+2:
        return 2
    else:
        return -2


def compute_align_score(inputMIDI, targetMIDI):
    print("len")
    print(len(inputMIDI))
    print(len(targetMIDI))
    
    alignScore = []
    for i in range(len(inputMIDI)+1):
        alignScore.append([-i])

    for i in range(1,len(targetMIDI)+1):
        alignScore[0].append(-i)

    for i in range(1,len(inputMIDI)+1):

        for j in range(1,len(targetMIDI)+1):
            alignScore[i].append(0)

            if i > 0:
                alignScore[i][j] = max(alignScore[i][j], alignScore[i-1][j]-1)
            if j > 0:
                alignScore[i][j] = max(alignScore[i][j], alignScore[i][j-1]-1)
            if i > 0 and j > 0:
                alignScore[i][j] = max(alignScore[i][j], match_score(inputMIDI[i-1], targetMIDI[j-1]) + alignScore[i-1][j-1])

    return alignScore[len(inputMIDI)][len(targetMIDI)]


def dynamic_programming(fundamental_freqs_query, target_song_name):

    queryMIDI = freqs_2_MIDI(fundamental_freqs_query)
    directory = "/Users/klaudiuszek/Desktop/Licencjat/Data/Testy/DB/" + target_song_name
    target = mido.MidiFile(directory, clip=True)
    
    tpb = target.ticks_per_beat
    lastTempo = target.tracks[0][0].tempo
    buckets = [[0 for i in range(2)] for j in range(len(target.tracks[0]))] 
    i = 0
    oldTime = 0
    absoluteTime = 0 
    absoluteTimes = []
    noteList = []

    for msg in target.tracks[0]:
        if not msg.is_meta:
            if msg.type == 'note_on':
              #  print(msg)
                noteList.append(msg.note)

    score = compute_align_score(queryMIDI, noteList)
    return score


if __name__ == "__main__":
    #song_name = "GdySlicznaPannaK"
    fund = [196.0,103.83,220.0,196.0,196.0,311.13,293.66,196.0,196.0,207.65,207.65,196.0,196.0,293.66,293.66,261.63]
    #nazwy = {"GdySlicznaPannaA", "GdySlicznaPannaK", "SzlaDzieweczkaA", "SzlaDzieweczkaK", "KawalekPodlogiA", "KawalekPodlogiK"}
    dynamic_programming(fund, "GdySlicznaPanna1.mid")
