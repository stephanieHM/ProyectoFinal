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
    # ,time.time()-inicio
    audioftt = np.fft.fft(a)
    freqs = np.fft.fftfreq(len(audioftt))
    idx = np.argmax(np.abs(audioftt))
    freq = freqs[idx]
    freq_in_hertz = abs(freq * wf.getframerate())
    print freq_in_hertz
	# print(freq_in_hertz)
        # print len(audio) #44100/4096=10.76 
	# print (freq.max(), freq.max())
    if freq_in_hertz <= 20:
        archivo.write("a\n")
        print("a")
    else: 
        if freq_in_hertz <= 40:
                archivo.write("v\n")
                print("v")	
        else:
           archivo.write("r\n")
           print("r") 
        
# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()


