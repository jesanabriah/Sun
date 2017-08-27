'''
Created on 26/08/2017

@author: Jorge Sanabria
'''

import libsun as sun
from scipy import misc

archivos = sun.ls("img/")

#mosaico.png en blanco
sun.resetMosaico()

for archivo in archivos:
    sun.procesar_imagen(archivo, 0.5)
    print ("Procesada: " + archivo)

print ("Procedimiento exitoso!!! :)")
