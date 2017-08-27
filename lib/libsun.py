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

    @contact: email: jesanabriah@unal.edu.co

    @organization: Universidad Nacional de Colombia
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
    filtro = img > median + (maximum - median) * factor
    img = img * filtro

    # Calcula los centros de masa con un maximo de NUM posibles manchas
    lbl, num = ndimage.label(img)

    # centros de masa
    center_of_mass = ndimage.measurements.center_of_mass(img, lbl, range(2, num + 1))

    # crear mapa de imagen con elementos calculados
    sun = misc.imread ("lib/img/" + file + "_1024.png", 1)
    mosaico = misc.imread ("output/mosaico_1024.png", 1)

    for elemento in center_of_mass:
        y = int(elemento[0])
        x = int(elemento[1])
        mosaico[y, x] = 0
        sun[y, x] = 0

    #configura un nuevo nombre para la imagen en output/
    archivo = archivo[:-9]
    archivo = archivo[:13] + ".png"

    misc.imsave("output/img/" + archivo, sun)
    misc.imsave("output/mosaico_1024.png", mosaico)

def resetMosaico():
    img = misc.imread ("lib/img/sun_1024.png")
    misc.imsave("output/mosaico_1024.png", img)
