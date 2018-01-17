#!/usr/bin/env python 

import subprocess


# Iterable con las rutas de los scripts
scripts_paths = ("/home/stephanie/ProyectoFinal/a1.py","/home/stephanie/ProyectoFinal/guarda.py","/home/stephanie/ProyectoFinal/leds.py")


# Creamos cada proceso    
procesos = [subprocess.Popen(["python", script]) for script in scripts_paths]


# Esperamos a que todos los subprocesos terminen.
for proceso in procesos:
    proceso.wait()

# Resto de codigo a ejecutar cuando terminen todos los subprocesos.
