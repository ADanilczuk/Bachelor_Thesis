
def findInTheFile(name):
    with open('Onsets.txt', 'r') as file:
        # Read all lines in the file one by one
        for line in file:
            # For each line, check if line contains the string
            if name in line:
                return line
    return ''

def loadOnsetData(line):
    # last two caracters from line are ';/n' so we dont need them
    # we split by ',' and remove first item in created array because it is a sound name
    onsets = line[:-2].split(',')[1:]
    # we need to map int() on this array due to taking the data from txt file
    onsets = list(map(int, onsets))
    return onsets

# name is just name of the file, without the .wav extension
onsets = findInTheFile(name) 
if onsets != '' :  
    onsets = loadOnsetData(onsets)
else:
    # calculate onsets with Envelope Match filter
    onsets = enf.get_onsets_locations(input_signal, window_size, threshold)
    onsets = enf.pick_best_onset_in_epsilon(onsets, 4000)