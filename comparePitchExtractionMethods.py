
import ProposedMethod
import KlaudiaPitch
import tryCepstralMethod
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
    
    (t1, (propsedFreqs, proposedNotes)) = mesureTimeAndExecute(ProposedMethod.calculatePitchExtraction, name)
    (t2, (KlaudiaFreqs, KlaudiaNotes)) = mesureTimeAndExecute(KlaudiaPitch.calculatePitchExtraction, name)
    (t3, (CepstralFreqs, CepstralNotes)) = mesureTimeAndExecute(tryCepstralMethod.calculatePitchExtraction, name, 1)
    (t4, (CepstralFreqs2, CepstralNotes2)) =  mesureTimeAndExecute(tryCepstralMethod.calculatePitchExtraction, name, 2)

    if version == 1:
        print("times", t1, t2, t3, t4)
        print("propsedFreqs", propsedFreqs)
        print("KlaudiaFreqs", KlaudiaFreqs)
        print("CepstralFreqs", CepstralFreqs)
        print("CepstralFreqs2", CepstralFreqs2)
        print("")
    
        print("proposedNotes", proposedNotes)
        print("KlaudiaNotes", KlaudiaNotes)
        print("CepstralNotes", CepstralNotes)
        print("CepstralNotes2", CepstralNotes2)

    

def chooseNotes(name):
    
    (propsedFreqs, proposedNotes) = ProposedMethod.calculatePitchExtraction(name)
    (KlaudiaFreqs, KlaudiaNotes) =  KlaudiaPitch.calculatePitchExtraction(name)
    (CepstralFreqs, CepstralNotes) = tryCepstralMethod.calculatePitchExtraction(name,1)
    (CepstralFreqs2, CepstralNotes2) = tryCepstralMethod.calculatePitchExtraction(name,2)

    preferedFreqs = KlaudiaFreqs
    preferedNotes = KlaudiaNotes
    
    notes = []
    freqs = []
    for i in range(len(CepstralNotes)):
        # nC- noteCandidates
        nC = [CepstralNotes[i], CepstralNotes2[i], proposedNotes[i], KlaudiaNotes[i]]
        b = Counter(nC)
        n = max(b)
        if b[n] == 1: 
            n = preferedNotes[i] 
        elif (b[n] == 2 and b[preferedNotes[i]] == 2 ):  
            n = preferedNotes[i]

        notes.append(n)
        freqs.append(note2Pitch(n))  

    return (freqs,notes)


if __name__ == "__main__": 
    name = "gdySlicznaPannaH2"
   
    (freqs, notes) = chooseNotes(name)
    print("freqs", freqs)
    print("notes", notes)
    # print(chooseNotes(name))

  
    
    
   
   
    
    
