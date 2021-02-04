import librosa
import numpy as np
import mido
import comparePitchExtractionMethods as cpem
import loadOnsetsFromFile as loff
import loadFreqsFromFile as leff
import itertools
import copy
from matplotlib import pyplot as plt
import music
from pylab import rcParams


# mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/"
mainPathDB = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/Kotek/"

rcParams['figure.figsize'] = 10, 7

def freqs_2_MIDI(freqs):

    midi = []
    for freq in freqs:
        m = 69 + 12 * np.log2(freq/440)
        midi.append(int(m))

    return midi


def midi2Freq(frequencyList):
    freq = []
    def f(midi):
        g = 2**(1/12)
        return 440*g**(midi-69)

    for midi in frequencyList:
        freq.append(round(f(midi), 2))
                
    return (freq)


def plotScalledFigures(targetMIDI, queryMIDI, timesInput, scaling):
    plotNotes = []
    plotTimes = []
    previous = []
    for noteList,time in targetMIDI:
        for n in noteList:
            plotNotes.append(n)
            plotTimes.append(time)

    figure, (ax1, ax2, ax3, ax4,ax5, ax6) = plt.subplots(6,1, True, True)
    figure.subplots_adjust(left=None, bottom=0.05, right=None, top=0.95, wspace=None, hspace=0.95)
    ax1.plot(plotTimes, plotNotes, 'o')
    ax1.set_title("Plik MIDI")
    plt.ylim([50,90])
    ax2.plot( list(map(lambda x: x*scaling[0], timesInput)), queryMIDI)
    ax2.set_title("Szukany sygnał skalowany przez 0.5")
    ax3.plot( list(map(lambda x: x*scaling[1], timesInput)), queryMIDI)
    ax3.set_title("Szukany sygnał skalowany przez 0.75")
    ax4.plot(timesInput, queryMIDI, label = "query")
    ax4.set_title("Oryginalny sygnał")
    ax5.plot( list(map(lambda x: x*scaling[3], timesInput)), queryMIDI)
    ax5.set_title("Szukany sygnał skalowany przez 1.25")
    ax6.plot( list(map(lambda x: x*scaling[4], timesInput)), queryMIDI)
    ax6.set_title("Szukany sygnał skalowany przez 1.5")
    # plt.savefig('../../grafiki/LinearScaling_gdySlicznaPannaS_plots.png')
    plt.show()


def calculate(queryMIDI, targetMIDI, timesInput):
    # scalingFactor - length ratio between the scaled and the original sequence
    # scalingFactorBounds -  the upper and lower bounds
    # resolution - the number of scaling factor     
    scalingFactor = 1 # ?
    resolution = 6
    scalingFactorBounds = [0.5, 1.5]
    step =  (scalingFactorBounds[1]/resolution)
    scaling = np.arange(scalingFactorBounds[0], scalingFactorBounds[1]+step,step).tolist()

    # plotScalledFigures(targetMIDI, queryMIDI, timesInput, scaling)

    maximal = 6
    matchingFactor = [0]*maximal
    i = 0
    queryIter = 0
    previous = []
    
    for factor in scaling:
        for noteList,time in targetMIDI:
            if (queryIter>=len(timesInput)-1): break
            if timesInput[queryIter]*factor+0.08 < time:
                # if queryIter< len(timesInput)-1: 
                    queryIter += 1
            if time >= timesInput[queryIter]*factor-0.08 \
                and time <= timesInput[queryIter]*factor+0.08: 
                if (queryMIDI[queryIter] in noteList) : #\
                    # or (queryMIDI[queryIter]+1 in noteList) \
                    # or (queryMIDI[queryIter]-1 in noteList):
                    matchingFactor[i] += 1
                    queryIter += 1
                elif (queryMIDI[queryIter] in previous):
                    matchingFactor[i] += 1
                    queryIter += 1
            previous = noteList
        i += 1
        queryIter = 0

 #maybe the note that appeared in query has just ended in target seconds ago, in this case it's almost a match so we want to count it
    # print("matchingFactor", matchingFactor)
    maxFactor = scaling[list.index(matchingFactor, max(matchingFactor))]
    # matching = []
    # for c in queryMIDI:
    #     for singleNote in targetMIDI[i]:
    #         if singleNote == c: 
    #             matching.append(c)
    #             continue
    #     i += 1
    # print("Maximal scaling factor and amount", maxFactor, matchingFactor )
    return (maxFactor, max(matchingFactor))




def linearScaling(fundamental_freqs_query, target_song_name, timesInput):
    queryMIDI = freqs_2_MIDI(fundamental_freqs_query)
    directory = mainPathDB + target_song_name
    target = mido.MidiFile(directory, clip=True)
    targetMIDI = []
    # tempo is time per quarter note = μs per quarter

    tpb = target.ticks_per_beat
    lastTempo = target.tracks[0][0].tempo
    # inSeconds = mido.tick2second(ticks, tpb, lastTempo)

    buckets = [[0 for i in range(2)] for j in range(len(target.tracks[0]))] 
    i = 0
    oldTime = 0
    absoluteTime = 0 
    absoluteTimes = []
    noteList = []
    for msg in target.tracks[0]:
        absoluteTime += msg.time
        if not msg.is_meta:
            if msg.type == 'note_on':  
                if msg.time != 0:
                    c =  copy.deepcopy(noteList)
                    buckets[i]=[c,oldTime]
                    i += 1
                    oldTime = round(mido.tick2second(absoluteTime, tpb, lastTempo) , 3)
                noteList.append(msg.note)
            elif msg.type == 'note_off':            
                if msg.time != 0:
                    c= copy.deepcopy(noteList)
                    buckets[i]=[c,oldTime]
                    i += 1
                    oldTime = round(mido.tick2second(absoluteTime, tpb, lastTempo), 3)
                noteList.remove(msg.note)
    buckets[i]=[noteList,oldTime]
    factor,score = calculate(queryMIDI, buckets[:i+1], timesInput)
    return (score, factor)


if __name__ == "__main__":
    name =  "GdySlicznaPannaA"
    song = mainPath + name + ".wav"
    # (freqsInput, _) = cpem.chooseNotes(name)
    timesInput = loff.loadOnsetFromFile(name)
    freqsInput = leff.loadFreqsFromFile(name)

    _, sr = librosa.load(song)
    timesInput = list(map(lambda x: x/sr, timesInput)) 
    linearScaling(freqsInput, "GdySlicznaPanna1.mid", timesInput)
    # linearScaling(freqs, "GdySlicznaPannaA", timesInput)
    # linearScaling(freqs, "KawalekPodlogiK", timesInput)