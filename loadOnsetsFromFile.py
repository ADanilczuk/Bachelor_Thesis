
import markThePlot as mtp

def findInTheFile(name):
    with open('Onsets.txt', 'r') as file:
        # Read all lines in the file one by one
        for line in file:
            # For each line, check if line contains the string
            if name in line:
                return line
    file.close()
    print("No onset data avaliable for this file")
    print("To mark it yourself write 1")
    print("To calculate write 2")
    inp = int(input())
    if inp == 1: 
        mtp.markOnsetsOnThePlot(name)
        return findInTheFile(name)
    else:
        return ''

def loadOnsetData(line):
    # last two caracters from line are ';/n' so we dont need them
    # we split by ',' and remove first item in created array because it is a sound name
    onsets = line[:-2].split(',')[1:]
    # we need to map int() on this array due to taking the data from txt file
    onsets = list(map(int, onsets))
    return onsets

def loadOnsetFromFile(name):
    onsets = findInTheFile(name)
    if onsets != '':
        return loadOnsetData(onsets)
    else: return ''


if __name__ == "__main__":    
    # name is just name of the file, without the .wav extension
    name = "piano1"
    onsets = findInTheFile(name) 
    if onsets != '' :  
        onsets = loadOnsetData(onsets)
    else:
        # calculate onsets with Envelope Match filter
        onsets = enf.get_onsets_locations(input_signal, window_size, threshold)
        onsets = enf.pick_best_onset_in_epsilon(onsets, 4000)