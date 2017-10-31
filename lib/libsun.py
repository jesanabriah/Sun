# -*- coding: utf-8 -*-
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
import time
import pickle

# Valores de configuracion del programa:
X, Y, YX, T = 1, 0, 0, 1

# Valor predeterminado para el error
XERR, DX_MIN, YERR = 6, 1, 2

# Lee objetos desde archivo
def load_data():
    try:
        with open("output/datos.dat") as f:
            datos = pickle.load(f)
    except:
        datos = {}
    return datos

# Guarda objetos en archivo
def save_data(data):
    with open("output/datos.dat", "wb") as f:
        pickle.dump(data, f)

# Crea lista con nombres de archivos
def ls(ruta='.'):
    '''
    Muestra la lista de archivos del directorio especificado.

    @return: Lista de nombres de archivos del directorio especificado.
    Si no especifica valor, muestra la lista de archivos del directorio actual.
    '''
    return listdir(ruta)

def getCMFromImage(archivo = "", factor = 0.5):
    '''
    A partir de archivo procesa una imagen del Sol,
    detectando los centros de masa con un factor
    por encima del valor medio y por debajo del maximo.

    @param archivo: la ruta del archivo a procesar

    @param factor: Desde 0 para valor promedio, hasta 1 para valor maximo

    @return: retorna centros de masa para la imagen
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
    #center_of_mass = ndimage.measurements.center_of_mass(img, lbl, range(2, num + 1))
    # El primer valor es el centro del Sol
    center_of_mass = ndimage.measurements.center_of_mass(img, lbl, range(1, num + 1))

    # lee el tiempo de toma de la imagen
    arch = archivo.split("_", 2)
    tiempo = time.strptime(arch[0] + arch[1], "%Y%m%d%H%M%S")

    # return centros de masa y tiempo de foto
    return center_of_mass, time.mktime(tiempo)

def resetMosaico(res):
    'Reset images output/mosaico_*.png with lib/img/sun_*.png'

    img = misc.imread ("lib/img/sun_" + res + ".png")
    misc.imsave("output/mosaico_" + res + ".png", img)

def getCenterofMassesofImages():
    #lee la lista de archivos
    archivos = ls("img/")

    # Los parametros recomendados son para imagenes de 4096
    # Procesa imagenes tipo *.jpg
    centers_of_masses = {}

    index = 0
    for archivo in archivos:
        if archivo[-4:] == ".jpg":
            centers_of_masses[index] = getCMFromImage(archivo)
            print "Procesada: " + archivo
            #print center_of_mass[index]
            index = index + 1

    return centers_of_masses


def getKey2(item):
    return item[2]

def getKey3(item):
    return item[3]

def get_ve_com(point, next_points):

    res = []

    for i in range(len(next_points)):
        #revisando xpos
        if next_points[i][X] > point[X] + DX_MIN: # El +DX_MIN asegura que la mancha si se mueva
            if next_points[i][X] < point[X] + XERR:
                #revisando ypos
                if next_points[i][Y] > point[Y] - YERR:
                    if next_points[i][Y] < point[Y] + YERR:
                        # y, x, dy, dx, index of next point
                        val = next_points[i][0], next_points[i][1], abs(next_points[i][Y] - point[Y]), abs(next_points[i][X] - point[X]), i
                        res.append(val)

    #primero ordenar
    res.sort(cmp=None, key=getKey3, reverse=False)
    res.sort(cmp=None, key=getKey2, reverse=False)

    try:
        return res[0]
    except IndexError:
        return ()

def getCenter(comsoi):

    promedio_x = 0
    promedio_y = 0

    # suma todos los valores de los centros de las imagenes
    for i in comsoi:
        promedio_x = promedio_x + comsoi[i][YX][0][X] #primer valor es el centro de la imagen
        promedio_y = promedio_y + comsoi[i][YX][0][Y] #primer valor es el centro de la imagen

    # calcula la cantidad de imagenes y divide para calcular el promedio
    tam = len(comsoi)
    promedio_x = promedio_x / tam
    promedio_y = promedio_y / tam

    return promedio_y, promedio_x

def get_ve_comsoi(coms, next_coms):

    ve_coms = []

    for i in range(len(coms[YX])):
        ve_coms.append(get_ve_com(coms[YX][i], next_coms[YX]))

    temp = next_coms[T], abs(next_coms[T] - coms[T])

    return ve_coms, temp

def get_ve_comsois(comsois):
    ve_comsois = {}
    #Calcula valores esperados para cada imagen
    for i in range(len(comsois) - 1):
        ve_comsois[i] = get_ve_comsoi(comsois[i], comsois[i + 1])

    return ve_comsois

def saveMosaico(ve_comsoi, res):
    #Dibujar mosaico
    print "Dibujando seguimiento de manchas en: output/mosaico_" + res + ".png"
    # mosaico_~.png en blanco
    resetMosaico(res)
    # Lee archivo
    mosaico = misc.imread ("output/mosaico_" + res + ".png", 1)
    # Dibuja linea con 3 puntos en (y, x), (y, x + 1), (y, x + 2)
    for i in ve_comsoi:
        for ve_com in ve_comsoi[i][YX]:
            try:
                y = int(ve_com[0])
                x = int(ve_com[1])
                mosaico[y, x] = 0
                mosaico[y, x + 1] = 0
                mosaico[y, x + 2] = 0
            except IndexError:
                pass
            except TypeError:
                pass
    # Guarda imagen procesada
    misc.imsave("output/mosaico_" + res + ".png", mosaico)

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
    mosaico = misc.imread ("output/mosaico_" + arch[2] + ".png", 1)

    for elemento in center_of_mass:
        y = int(elemento[0])
        x = int(elemento[1])
        mosaico[y, x] = 0
        sun[y, x] = 0

    #configura un nuevo nombre para la imagen en output/
    archivo = arch[0] + "_" + arch[1] + "_" + arch[2] + ".png"

    misc.imsave("output/img/" + archivo, sun)
    misc.imsave("output/mosaico_" + arch[2] + ".png", mosaico)
