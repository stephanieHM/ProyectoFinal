import pyaudio
import numpy as np
from matplotlib import use
import  matplotlib.pyplot as plt
import matplotlib.animation as animation
import wave
import struct
import time

SEGUNDOS = 10 
MILISEGUNDOS_GRABACION = SEGUNDOS*1000
CHUNK = 2**12 #Tamaño de ventana
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 44100 #Frecuencia de muestreo 

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

# Tiempo de inicio de grabación 
inicio=time.time()

# Función donde se realiza la grabación de audio
def generador():
    i = generador.i
    t=0
    data = wf.readframes(CHUNK)
    while t < 12: # Tiempo de grabación 
	data = stream.read(CHUNK)
	t=time.time()-inicio
        audio = np.fromstring(data, np.int16)
        tiempo = np.arange((CHUNK * i), audio.shape[0] + (CHUNK * i))/float(RATE)
        i += 1
	audioftt = np.fft.fft(audio) # Transformada de Fourier
	freqs = np.fft.fftfreq(len(audioftt))
	idx = np.argmax(np.abs(audioftt)) # Frecuencia característica
	freq = freqs[idx]
	freq_in_hertz = abs(freq * wf.getframerate()) # Frecuencia en Hz
	print freq_in_hertz
        if freq_in_hertz <= 100: #Nivel bajo, led blanco
                gpio.setmode(gpio.BCM)
                gpio.setup(15,gpio.OUT)
                gpio.output(15,gpio.HIGH)
                time.sleep(1)
                gpio.output(15,gpio.LOW)
                
        else: 
                if freq_in_hertz <= 1000: #Nivel medio, led verde
                        gpio.setmode(gpio.BCM)    
                        gpio.setup(18,gpio.OUT)
                        gpio.output(18,gpio.HIGH)
                        time.sleep(1)
                        gpio.output(18,gpio.LOW)	
                else:
                        gpio.setmode(gpio.BCM) #Nivel alto, led rojo
                        gpio.setup(23,gpio.OUT)
                        gpio.output(23,gpio.HIGH)
                        time.sleep(1)
                        gpio.output(23,gpio.LOW)

	yield tiempo, audio, audioftt #Datos para graficar
generador.i = 0

# Función para graficar
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

    return line, line2

ani = animation.FuncAnimation(fig, animacion, generador, blit=True,
interval=50, repeat=False)
plt.show()

