try:
    import pyaudio
    import numpy as np
    from matplotlib import use
    import  matplotlib.pyplot as plt
    import matplotlib.animation as animation
except ImportError:
    raise ImportError('Faltan modulos externos que instalar')
import wave
import struct
import time

SEGUNDOS = 10
MILISEGUNDOS_GRABACION = SEGUNDOS*1000
NOMBRE_ARCHIVO_WAV = "output.wav"

CHUNK = 2**12
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
frames = []

# Definicion de la figura (matplotlib)
fig = plt.figure()
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
line, = ax.plot(0, 0, lw=2)
line2, =ax2.plot(0,0, lw=2)

# Limites de los ejes
ax.set_xlim(0, MILISEGUNDOS_GRABACION/1000)
ax.set_ylim(-5000, 5000)
ax2.set_xlim(0, MILISEGUNDOS_GRABACION/1000)
ax2.set_ylim(-50000, 50000)

# Generar primer plot vacio
xdata = None
ydata = None
xdata2 = None
ydata2 = None

# Iniciar stream de audio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
inicio=time.time()
def generador():
    i = generador.i
    t=0
    characFreq = []
    while t < 5:# i < range(0, int(RATE / CHUNK * (SEGUNDOS))):
        data = stream.read(CHUNK)
	t=time.time()-inicio
        audio = np.fromstring(data, np.int16)
        tiempo = np.arange((CHUNK * i), audio.shape[0] + (CHUNK * i))/float(RATE)
        i += 1
	audioftt = np.fft.fft(audio)
	freqs = np.fft.fftfreq(len(audioftt))
	idx = np.argmax(np.abs(audioftt))
	freq = freqs[idx]
	freq_in_hertz = abs(freq * RATE)
	# print(freq_in_hertz)
        # print len(audio) #44100/4096=10.76 
	# print (freq.max(), freq.max())
        yield tiempo, audio, audioftt
	characFreq.append(freq_in_hertz)
    print(characFreq)
    print len(characFreq)
generador.i = 0

def animacion(data):
    x, y, yf = data
    global xdata
    global ydata
    global xdata2
    global ydata2
    if xdata == None:
        xdata = x
        ydata = y
    else:
        xdata = np.append(xdata, x)
        ydata = np.append(ydata, y)
        xdata2 = np.append(xdata, x)
        ydata2 = np.append(ydata, yf)
    global line
    line.set_data(xdata, ydata)
    line2.set_data(xdata2, ydata2)

    return line,

ani = animation.FuncAnimation(fig, animacion, generador, blit=True,
interval=50, repeat=False)
plt.show()
