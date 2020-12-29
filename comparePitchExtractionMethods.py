
import ProposedMethod
import KlaudiaPitch
import tryCepstralMethod
import time
from collections import Counter

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
    
    (_, proposedNotes) = ProposedMethod.calculatePitchExtraction(name)
    (_, KlaudiaNotes) = KlaudiaPitch.calculatePitchExtraction(name)
    (_, CepstralNotes) = tryCepstralMethod.calculatePitchExtraction(name,1)
    (_, CepstralNotes2) = tryCepstralMethod.calculatePitchExtraction(name,2)

    prefered = KlaudiaNotes
    
    notes = []
    voter = None
    for i in range(len(CepstralNotes)):
        noteCandidates = [CepstralNotes[i], CepstralNotes2[i], proposedNotes[i], KlaudiaNotes[i]]
        b = Counter(noteCandidates)
        n = max(b)
        if b[n] == 1: n = prefered[i]
        elif (b[n] == 2 and b[prefered[i]] == 2 ):  n = prefered[i]
        notes.append(n)
    return notes


if __name__ == "__main__": 
    name = "gdySlicznaPannaH2"
   
    # comparePitchResults(name, 1)
    print(chooseNotes(name))
  
    
    
   
   
    
    
