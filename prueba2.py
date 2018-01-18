import wave
import struct
import numpy as np

CHUNK = 2**12
frate = 44100

fileName = "whitenoise.wav"
wav_file = wave.open(fileName, "r")
data = wav_file.readframes(CHUNK)
wav_file.close()
data = struct.unpack('{n}h'.format(n=CHUNK), data)
data = np.array(data)

w = np.fft.fft(data)
freqs = np.fft.fftfreq(len(w))
print(freqs.min(), freqs.max())

# Find the peak in the coefficients
idx = np.argmax(np.abs(w))
freq = freqs[idx]
freq_in_hertz = abs(freq * frate)
print(freq_in_hertz)
