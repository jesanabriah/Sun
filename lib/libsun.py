'''
Created on 27/08/2017

    Sun - Rotacion diferencial del Sol

    @copyright: Copyright (C) 2017 Jorge Sanabria

    @author: Jorge Sanabria

    @license: GNU General Public License version 3

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    @contact: jesanabriah@unal.edu.co

    @organization: Universidad Nacional de Colombia
'''

from os import listdir
from scipy import misc
from scipy import ndimage

def ls(ruta='.'):
    '''
    Muestra la lista de archivos del directorio especificado.

    @return: Lista de nombres de archivos del directorio especificado.
    Si no especifica valor, muestra la lista de archivos del directorio actual.
    '''
    return listdir(ruta)

def procesar_imagen(archivo = "", factor = 0.5, file = "white"):
    '''
    A partir de archivo procesa una imagen del Sol,
    detectando los centros de masa con un factor
    por encima del valor medio y por debajo del maximo.

    Crea un archivo procesado en la carpeta output/img/~.png
    y otro en output/mosaico_~.png con una
    superpocision de todos los valores.

    @param archivo: la ruta del archivo a procesar

    @param factor: Desde 0 para valor promedio, hasta 1 para valor maximo

    @param file: puede ser 'white' para usar white_~.png o 'sun' para usar sun_~.png
    '''

    # Lee la imagen del disco duro
    img = misc.imread ("img/" + archivo, 1)

    # Calcula el valor maximo de intensidad para un pixel e invierte todos los valores, de modo que ahora oscuridad = max y luz = 0
    maximum = ndimage.maximum(img)
    img = maximum - img

    # calcula para los nuevos datos maximo y valor promedio
    median = ndimage.median(img)
    maximum = ndimage.maximum(img)

    # Crea filtro con un criterio muy relativo :P
    filtro = img > median + (maximum - median) * factor
    img = img * filtro

    # Calcula los centros de masa con un maximo de NUM posibles manchas
    lbl, num = ndimage.label(img)

    # centros de masa
    center_of_mass = ndimage.measurements.center_of_mass(img, lbl, range(2, num + 1))

    # crear mapa de imagen con elementos calculados
    arch = archivo.split("_", 3)
    sun = misc.imread ("lib/img/" + file + "_" + arch[2] + ".png", 1)
    mosaico = misc.imread ("output/mosaico_1024.png", 1)

    for elemento in center_of_mass:
        y = int(elemento[0])
        x = int(elemento[1])
        mosaico[y, x] = 0
        sun[y, x] = 0

    #configura un nuevo nombre para la imagen en output/
    archivo = archivo[:13] + ".png"

    misc.imsave("output/img/" + archivo, sun)
    misc.imsave("output/mosaico_" + arch[2] + ".png", mosaico)

def resetMosaico():
    'Reset images output/mosaico_*.png with lib/img/sun_*.png'

    img = misc.imread ("lib/img/sun_512.png")
    misc.imsave("output/mosaico_512.png", img)

    img = misc.imread ("lib/img/sun_1024.png")
    misc.imsave("output/mosaico_1024.png", img)
