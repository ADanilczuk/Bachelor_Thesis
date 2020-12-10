from matplotlib import pyplot as plt

import librosa
import math
import numpy as np

Onsets = []
input_signal = None
time = None
fig = None
y = None

def onclick(event):
    global Onsets, fig
    elementNumber = int(round((event.xdata * len(input_signal) )/time[len(time)-1] ))
    print('elementNumber, timeStamp ', elementNumber, time[len(time)-1]  )
   
    Onsets.append(elementNumber)
    plt.plot([event.xdata]*2, y, '-')
    fig.canvas.draw()


def markOnsetsOnThePlot(name):
    global input_signal, time, fig, y
    song =  "C:/Alusia/Studia/Praca Dyplomowa/data/"+name +".wav"
    
    input_signal, sr = librosa.load(song)
    time = np.arange(0, len(input_signal)) / sr
    fig = plt.figure(1)
    plt.plot(time, input_signal)

    y = np.linspace(min(input_signal),max(input_signal),2)
   
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    Onsets.sort()
    # Save new song data to the file (we assume that if this function is ran this song is not yet in the dataset)
    with open('Onsets.txt', 'a') as file:
        file.write(name +',')
        for i in range(len(Onsets)-2):
            file.write("%s," % Onsets[i])
        print(Onsets[len(Onsets)-2])
        file.write("%s;\n" % Onsets[len(Onsets)-2])
    print(Onsets)

markOnsetsOnThePlot("tamNaDnieS")