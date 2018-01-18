"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import numpy as np
import time

CHUNK = 1024

wf = wave.open("/home/stephanie/ProyectoFinal/whitenoise.wav", 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data
data = wf.readframes(CHUNK)

# inicio=time.time
# play stream (3)
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)
    a=np.fromstring(data,'Int16')
    print a# ,time.time()-inicio

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()


