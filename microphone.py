#!/usr/bin/python
# -*- coding: utf-8 -*-�
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
		starting_point = time.time()
		print ("time is...")		
		print starting_point
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
        wf = wave.open('audio.wav', 'wb') #Archivo wav donde se procesa el audio grabado
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()
        return True

if __name__ == '__main__':
    mic = Microphone()
    while True:
        if  mic.passiveListen('ok Google'):
            fs, data = wavfile.read('audio.wav')
            L = len(data)
            c = np.fft.fft(data) # create a list of complex number
            freq = np.fft.fftfreq(L)
            #freq = np.linspace(0, 1/(2L), L/2)
            print ("frecuencia 1 ")
	    print freq
            freq_in_hertz = abs(freq * fs)
	    print freq_in_hertz
            plt.plot(freq_in_hertz, abs(c))
            plt.show()
	    final_point = time.time()
	    print ("time final is...")		
	    print final_point
