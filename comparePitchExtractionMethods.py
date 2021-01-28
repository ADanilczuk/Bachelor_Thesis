
import thirdBiggestFft
import harmonicProduct
import cepstralMethod
import autocorrelationFunction
import averageMagnitudeDifferenceFunction
import SaveDataInTxt as sd

import time
from collections import Counter
from math import log2, pow
import re 

A4 = 440
C0 = A4*pow(2, -4.75)
noteName = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def pitch2Note(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return noteName[n] + str(octave)


def note2Pitch(note): 
    temp = re.compile("([a-zA-Z]?#?)([0-9]+)") 
    res = temp.match(note).groups() 
    nt = res[0]
    octave = int(res[1])
    idx = noteName.index(res[0])
    idx = idx + 4 + ((octave - 1) * 12); 

    return round((A4 * 2** ((idx- 49) / 12)),2)

def mesureTimeAndExecute(function, *args):
    tic = time.perf_counter()
    (freqs, notes) = function(*args)
    toc = time.perf_counter()
    t = toc - tic
    
    return  (t, (freqs, notes))

def comparePitchResults(name, version):
    
    
    (t1, (ThirdFreqs, ThirdNotes)) = mesureTimeAndExecute(thirdBiggestFft.calculatePitchExtraction, name)
    (t2, (HarmonicFreqs, HarmonicNotes)) = mesureTimeAndExecute(harmonicProduct.calculatePitchExtraction, name)
    (t3, (CepstralFreqs, CepstralNotes)) = mesureTimeAndExecute(cepstralMethod.calculatePitchExtraction, name, 1)
    (t4, (CepstralFreqs2, CepstralNotes2)) =  mesureTimeAndExecute(cepstralMethod.calculatePitchExtraction, name, 2)

    (t5, (ACFFreqs, ACFNotes)) = mesureTimeAndExecute(autocorrelationFunction.calculatePitchExtraction, name)
    (t6, (AMDFFreqs, AMDFNotes)) = mesureTimeAndExecute(averageMagnitudeDifferenceFunction.calculatePitchExtraction, name)
    
    (_, choosenNotes) = chooseNotesFromArgs(ThirdNotes, CepstralNotes, CepstralNotes2, HarmonicNotes)

    if version == 1:
        # print("times", t1, t2, t3, t4, t5, t6)
        # print("propsedFreqs", ThirdFreqs)
        # print("KlaudiaFreqs", HarmonicFreqs)
        # print("CepstralFreqs", CepstralFreqs)
        # print("CepstralFreqs2", CepstralFreqs2)
        # print("")
    
        print("proposedNotes", ThirdNotes)
        print("HarmonicNotes", HarmonicNotes)
        print("CepstralNotes", CepstralNotes)
        print("CepstralNotes2", CepstralNotes2)
        print("ACFNotes", ACFNotes)
        print("AMDFNotes", AMDFNotes)
        print("Finally choosen", choosenNotes)

    space = ' & '
    fileName = 'NoteCalculations'
    sd.saveInTxt(fileName, name, ACFNotes, space, 'AF')
    sd.saveInTxt(fileName, '', AMDFNotes, space, 'AMDF')
    sd.saveInTxt(fileName, '', CepstralNotes, space, 'C1')
    sd.saveInTxt(fileName, '', CepstralNotes2, space, 'C2')
    sd.saveInTxt(fileName, '', HarmonicNotes, space, 'HP')
    sd.saveInTxt(fileName, '', ThirdNotes, space, '3BF')
    sd.saveInTxt(fileName, '', choosenNotes, space, 'Wynik')
    
def chooseNotesFromArgs(ThirdNotes, CepstralNotes, CepstralNotes2, HarmonicNotes):
    preferedFreqs = HarmonicNotes
    preferedNotes = HarmonicNotes
    
    notes = []
    freqs = []
    for i in range(len(CepstralNotes)):
        # nC- noteCandidates
        nC = [CepstralNotes[i], CepstralNotes2[i], ThirdNotes[i], HarmonicNotes[i]]
        b = Counter(nC)
        n = max(b)
        if b[n] == 1: 
            n = preferedNotes[i] 
        elif (b[n] == 2 and b[preferedNotes[i]] == 2 ):  
            n = preferedNotes[i]

        notes.append(n)
        freqs.append(note2Pitch(n))  

    return (freqs,notes)


def chooseNotes(name, version=0):
    
    (ThirdFreqs, ThirdNotes) = thirdBiggestFft.calculatePitchExtraction(name)
    (HarmonicFreqs, HarmonicNotes) =  harmonicProduct.calculatePitchExtraction(name)
    (CepstralFreqs, CepstralNotes) = cepstralMethod.calculatePitchExtraction(name,1)
    (CepstralFreqs2, CepstralNotes2) = cepstralMethod.calculatePitchExtraction(name,2)

    preferedFreqs = HarmonicFreqs
    preferedNotes = HarmonicNotes
    
    notes = []
    freqs = []
    for i in range(len(CepstralNotes)):
        # nC- noteCandidates
        nC = [CepstralNotes[i], CepstralNotes2[i], ThirdNotes[i], HarmonicNotes[i]]
        b = Counter(nC)
        n = max(b)
        if b[n] == 1: 
            n = preferedNotes[i] 
        elif (b[n] == 2 and b[preferedNotes[i]] == 2 ):  
            n = preferedNotes[i]

        notes.append(n)
        freqs.append(note2Pitch(n))  

    if (version ==1):
        space = ','
        fileName = 'FrequenciesCalculations'
        sd.saveInTxt(fileName, name, freqs, space)

    return (freqs,notes)


if __name__ == "__main__": 
    nazwy = {"GdySlicznaPannaA", "GdySlicznaPannaK", "SzlaDzieweczkaA", "SzlaDzieweczkaK", "KawalekPodlogiA", "KawalekPodlogiK"}
    # for name in nazwy:
    #     comparePitchResults(name, 1)
    #     print("ok", name)
    
    chooseNotes("WlazlKotekA", 1)

    # for name in nazwy:
    #     chooseNotes(name, 1)
    #     print("ok", name)


  
    
    
   
   
    
    
