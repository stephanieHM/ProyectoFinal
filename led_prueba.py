import RPi.GPIO as gpio


gpio.setmode(gio.BCM)
gpio.setup(14,gpio.OUT)
gpio.output(14,gpio.HIGH) 
gpio.output(14,gpio.LOW)  
	


