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
CHUNK = 2**12 #Tamano de ventana
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

# Apertura de archivo .WAV en modo de lectura
wf = wave.open("/home/stephanie/ProyectoFinal/voz.wav", 'rb')

# Iniciar stream de audio
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
archivo = open("frecuencias.txt", "w")
# Tiempo de inicio de lectura del archivo .WAV
inicio=time.time()

# Funcion donde se genera la reproduccion de audio
def generador():
    i = generador.i
    t=0
    characFreq=[]
    data = wf.readframes(CHUNK)
    while t < 12: # Tiempo de reproduccion menor a 12 segundos
	stream.write(data)
        data = wf.readframes(CHUNK)
	t=time.time()-inicio
        audio = np.fromstring(data, np.int16)
        tiempo = np.arange((CHUNK * i), audio.shape[0] + (CHUNK * i))/float(RATE)
        i += 1
	audioftt = np.fft.fft(audio) # Transformada de Fourier
	freqs = np.fft.fftfreq(len(audioftt))
	idx = np.argmax(np.abs(audioftt)) # Frecuencia caracteristica
	freq = freqs[idx]
	freq_in_hertz = abs(freq * wf.getframerate()) # Frecuencia en Hz
	print freq_in_hertz
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
	yield tiempo, audio, audioftt

  
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

    return line, line2

ani = animation.FuncAnimation(fig, animacion, generador, blit=True,
interval=50, repeat=False)
plt.show()
archivo.close()
