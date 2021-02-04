import librosa
import linearScaling
import loadFreqsFromFile as leff
import loadOnsetsFromFile as loff
import os
import saveDataInTxt as sd

import time
from collections import Counter
from math import log2, pow
import re 

# mainPath = "/Users/klaudiuszek/Desktop/Licencjat/Data/" 
mainPath = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/"
mainPathDatabase = "C:/Alusia/Studia/Praca Dyplomowa/data/Testy/Kotek/"



def showLinearScalingResults(analyzedSongName):
    dbSongNames = os.listdir(mainPathDatabase)
    # print(dbSongNames)
    song = mainPath + analyzedSongName + ".wav"

    timesInput = loff.loadOnsetFromFile(analyzedSongName)
    _, sr = librosa.load(song)
    timesInput = list(map(lambda x: x/sr, timesInput)) 
    freqsInput = leff.loadFreqsFromFile(analyzedSongName)
    
    space = ' & '
    fileName = 'MelodyCalculations'
    i = 0

    print(analyzedSongName)
    for dbSong in dbSongNames:
        (score, factor) = linearScaling.linearScaling(freqsInput, dbSong, timesInput)
        print(dbSong, score, factor)
        # if i==0:
        #     sd.saveInTxt(fileName, name, [score, factor], space, dbSong)
        #     i  = 2
        # else: 
        #     sd.saveInTxt(fileName, '', [score, factor], space, dbSong)

    

if __name__ == "__main__": 

    nazwy = {"GdySlicznaPannaA", "GdySlicznaPannaK", "SzlaDzieweczkaA", "SzlaDzieweczkaK", "KawalekPodlogiA", "KawalekPodlogiK"}
    # for name in nazwy:
    #     showLinearScalingResults(name)
    #     print()
  
    showLinearScalingResults("WlazlKotekK")