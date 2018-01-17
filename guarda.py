
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
np.savetxt('archivo.txt', freq2, fmt='%.4e')
#plt.plot(freq2[:500])
#plt.title('freq 2')
#plt.show()

