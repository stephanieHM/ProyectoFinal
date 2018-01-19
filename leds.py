#import RPi.GPIO as gpio


f=open("frecuencias.txt", "r")

while True: 
	linea = f.readline()
	if not linea: break
	print linea

	if linea == "a\n":
		print "am"
	elif linea == 'v\n':
		print "ve"
	else: 
		print "ro"

		
		#gpio.setmode(gio.BCM)
		#gpio.setup(14,gpio.OUT)
		#gpio.output(14,gpio.HIGH) ----encender el led
		#gpio.output(14,gpio.LOW) ----apagar pag. 232 
	
f.close()

