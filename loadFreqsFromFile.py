
import comparePitchExtractionMethods as cpe

def findInTheFile(name):
    c = False
    with open('FrequenciesCalculations.txt', 'r') as file:
        # Read all lines in the file one by one
        for line in file:
            if c: return line
            # For each line, check if line contains the string
            if name in line:
                c = True
    file.close()
    print("No frequency data avaliable for this file")
    print("To calculate it yourself write 1")
    print("To calculate it by default 2")
    inp = int(input())
    if inp == 1: 
        return ''
    else:
        (_,_) = cpe.chooseNotes(name, 1)
        return findInTheFile(name)

def loadFreqsData(line):
    # last two caracters from line are ';/n' so we dont need them
    # we split by ',' and remove first item in created array because it is a sound name
    freqs = line[:-4].split(',')
    # we need to map int() on this array due to taking the data from txt file
    freqs = list(map(float, freqs))
    return freqs

def loadFreqsFromFile(name):
    freqs = findInTheFile(name)
    if freqs != '':
        return loadFreqsData(freqs)
    else: return ''


if __name__ == "__main__":    
    # name is just name of the file, without the .wav extension
    # name = "piano1"
    nazwy = {"GdySlicznaPannaA", "GdySlicznaPannaK", "SzlaDzieweczkaA", "SzlaDzieweczkaK", "KawalekPodlogiA", "KawalekPodlogiK"}
    for name in nazwy:
        freqs = findInTheFile(name) 
        if freqs != '' :  
            freqs = loadFreqsData(freqs)
        else: 
            print("else")
        print(name, freqs, len(freqs))
        # calculate onsets with Envelope Match filter
        # onsets = enf.get_onsets_locations(input_signal, window_size, threshold)
        # onsets = enf.pick_best_onset_in_epsilon(onsets, 4000)