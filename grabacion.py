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
ax = fig.add_subplot(111)

line, = ax.plot(0, 0, lw=2)

# Limites de los ejes
ax.set_xlim(0, MILISEGUNDOS_GRABACION/1000)
ax.set_ylim(-5000, 5000)


# Generar primer plot vacio
xdata = None
ydata = None


# Iniciar stream de audio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)


archivo = open("frecuencias.txt", "w")
inicio=time.time()

def generador():
    i = generador.i
    t=0
    characFreq = []
    j=0
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
        characFreq.append(freq_in_hertz)
	yield tiempo, audio

  
generador.i = 0

def animacion(data):
    x, y = data
    global xdata
    global ydata
 
    if xdata == None:
        xdata = x
        ydata = y
    else:
        xdata = np.append(xdata, x)
        ydata = np.append(ydata, y)

    global line
    line.set_data(xdata, ydata)


    return line,

ani = animation.FuncAnimation(fig, animacion, generador, blit=True,
interval=50, repeat=False)
plt.show()
archivo.close()
