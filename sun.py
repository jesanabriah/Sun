'''
Created on 26/08/2017

@author: Jorge Sanabria
'''

from scipy import misc

import libsun as sun


archivos = sun.ls("img/")

#mosaico.png en blanco
sun.resetMosaico()

for archivo in archivos:
    sun.procesar_imagen(archivo, 0)
    print ("Procesada: " + archivo)

print ("Procedimiento exitoso!!! :)")
