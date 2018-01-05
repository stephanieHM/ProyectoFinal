import RPi.GPIO as gpio

archivo = open("frecuencias.txt", “w”)
archivo.read()
archivo.close() 

gpio.setmode(gio.BCM)
gpio.setup(14,gpio.OUT)
gpio.output(14,gpio.HIGH) ----encender el led
gpio.output(14,gpio.LOW) ----apagar pág. 232 
exit()
