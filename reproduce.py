
import matplotlib.pyplot as plt # For visualizing the data and error
from sklearn import datasets #Sklearn library for load data
import numpy as np #Numpy array
from matplotlib.colors import ListedColormap # Content list of color for plotting
from scipy.io import wavfile

import pyaudio
import numpy as np


volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 10.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float


### LOAD NOISE DATASET

fs, noise = wavfile.read('whitenoise.wav')
L = len(noise)
c = np.fft.fft(noise) # create a list of complex number
freq2 = (np.abs(c[:len(c)])) #-----

####AUDIO
p = pyaudio.PyAudio()

# generate samples, note conversion to float32 array
samples = freq2.astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)


# play. May repeat with different volume values (if done interactively) 
stream.write(volume*freq2)
print (stream.write(volume*freq2))


stream.stop_stream()
stream.close()

p.terminate()

