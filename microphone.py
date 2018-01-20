#!/usr/bin/python
# -*- coding: utf-8 -*- 
import pyaudio
import struct
import math
import wave
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.io import wavfile
#import urllib  
#import urllib2 
import os

class Microphone:

    def rms(self,frame):

        count = len(frame)/2
        format = "%dh"%(count)
        shorts = struct.unpack( format, frame )
        sum_squares = 0.0
        for sample in shorts:
            n = sample * (1.0/32768.0)
            sum_squares += n*n
        rms = math.pow(sum_squares/count,0.5);
        return rms * 1000

    def passiveListen(self,persona): 
	
	#Espera para el audio, threshold define el umbral

        CHUNK = 1024; RATE = 8000; THRESHOLD = 0; LISTEN_TIME = 12
        didDetect = False
        # prepare recording stream
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
        # stores the audio data
        all =[]
        # starts passive listening for disturbances 
        print RATE / CHUNK * LISTEN_TIME
        for i in range(0, RATE / CHUNK * LISTEN_TIME):
            input = stream.read(CHUNK)
            rms_value = self.rms(input)
            print rms_value
            if (rms_value >= THRESHOLD):
                didDetect = True

                print "Listening...\n"
                break
        if not didDetect:
            stream.stop_stream()
            stream.close()
            return False
        # append all the chunks
        all.append(input)
        for i in range(0, 100): #El num. 100 ajusta la duracion (aprox. 12 segundos en este caso)
            data = stream.read(CHUNK)
            all.append(data)
        # save the audio data   
        data = ''.join(all)
        stream.stop_stream()
        stream.close()
        wf = wave.open('voz.wav', 'wb') #Archivo wav donde se procesa el audio grabado
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(data)
	print wf
        wf.close()
        return True

if __name__ == '__main__':
    mic = Microphone()
    flag=True
    while flag:
        if  mic.passiveListen('ok Google'):
            fs, data = wavfile.read('voz.wav')
            L = len(data)
            c = np.fft.fft(data) # create a list of complex number
            freq = np.fft.fftfreq(L)

	    freq2 = (np.abs(c[:len(c)]))
            plt.plot(freq2[:500])
	    plt.show()

            #freq = np.linspace(0, 1/(2L), L/2)
            print ("frecuencia 1 ")
	    print freq

	
            freq_in_hertz = abs(freq * fs)
	    print freq_in_hertz
	    print len(freq_in_hertz)
	    print abs(c)
	    print len(abs(c))

            plt.plot(freq_in_hertz[:500], abs(c)[:500])
            plt.show()
	    
	    flag=False

