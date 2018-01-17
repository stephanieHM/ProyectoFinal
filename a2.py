"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import numpy as np
from scipy.io import wavfile
CHUNK = 1024
frames1 = []

wf = wave.open("/home/stephanie/ProyectoFinal/whitenoise.wav", 'r')


# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data

wf2 = wavfile.read("/home/stephanie/ProyectoFinal/audio.wav")

data = wf.readframes(CHUNK)

while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)
    L = len(data)
    a=np.fromstring(data,'Int16')
    

    #c=np.fft.fft(a) 
    #freq2 = (np.abs(c[:len(c)]))

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()


