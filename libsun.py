'''
Created on 27/08/2017

@author: Jorge Sanabria
'''

from os import listdir
from scipy import misc
from scipy import ndimage

def ls(ruta='.'):
    return listdir(ruta)

def procesar_imagen(archivo, factor = 0.5, file = "white"):

    # Lee la imagen del disco duro
    img = misc.imread ("img/" + archivo, 1)

    # Calcula el valor maximo de intensidad para un pixel e invierte todos los valores, de modo que ahora oscuridad = max y luz = 0
    maximum = ndimage.maximum(img)
    img = maximum - img

    # calcula para los nuevos datos maximo y valor promedio
    median = ndimage.median(img)
    maximum = ndimage.maximum(img)

    # Crea filtro con un criterio muy relativo :P
    filtro = img > (median + maximum) * factor
    img = img * filtro

    # Calcula los centros de masa con un maximo de NUM posibles manchas
    lbl, num = ndimage.label(img)

    # centros de masa
    center_of_mass = ndimage.measurements.center_of_mass(img, lbl, range(2, num + 1))

    # crear mapa de imagen con elementos calculados
    sun = misc.imread (file + ".png", 1)
    mosaico = misc.imread ("mosaico.png", 1)

    for elemento in center_of_mass:
        y = int(elemento[0])
        x = int(elemento[1])
        mosaico[y, x] = 0
        sun[y, x] = 0

    #configura un nuevo nombre para la imagen en output/
    archivo = archivo[:-9]
    archivo = archivo[:13] + ".png"

    misc.imsave("output/" + archivo, sun)
    misc.imsave("mosaico.png", mosaico)

def resetMosaico():
    img = misc.imread ("sun.png")
    misc.imsave("mosaico.png", img)
