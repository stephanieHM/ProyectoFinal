try:
    import pyaudio
    import numpy as np
    from matplotlib import use
    import  matplotlib.pyplot as plt
    import matplotlib.animation as animation
except ImportError:
    raise ImportError('Faltan modulos externos que instalar')

import wave

SEGUNDOS = 10
MILISEGUNDOS_GRABACION = SEGUNDOS*1000
NOMBRE_ARCHIVO_WAV = "whitenoise.wav"

wf = wave.open("/home/stephanie/ProyectoFinal/whitenoise.wav", 'rb')

CHUNK = 2**10
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
ax.set_ylim(-50000, 50000)

# Generar primer plot vacio
xdata = None
ydata = None

# Iniciar stream de audio
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)


def generador():
    i = generador.i
    data = wf.readframes(CHUNK)
    while i < range(0, int(RATE / CHUNK * (SEGUNDOS))):# len(data)>0: #i < range(0, int(RATE / CHUNK * (SEGUNDOS))):
        stream.write(data)
        data = wf.readframes(CHUNK)
        audio = np.fromstring(data,'Int16')
        c = np.fft.fft(audio)
	a=abs(c) 
        #freq2 = (np.abs(c[:len(c)]))
        #print freq2
        tiempo = np.arange((CHUNK * i), audio.shape[0] + (CHUNK * i))/float(wf.getframerate())
        i += 1
        #print audio
        yield tiempo, audio
	print a
	#a=np.fft.fftfreq(len(audio))
	#freq_in_hertz = abs(a * wf.getframerate())
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
    #print xdata
    #print ydata

    return line,

ani = animation.FuncAnimation(fig, animacion, generador, blit=True,
interval=50, repeat=False)
plt.show()

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
