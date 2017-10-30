'''
Created on 26/08/2017

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
from scipy.ndimage.measurements import center_of_mass
from os import listdir
from scipy import misc
from scipy import ndimage
import time

# Valores de configuracion del programa:
X = 1
Y = 0
YX = 0
T = 1
# Valor predeterminado para el error en x
XERR = 6
DX_MIN = 0.7
# Valor predeterminado para el error en y
YERR = 2

center = 0, 0

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
    center_of_mass = ndimage.measurements.center_of_mass(img, lbl, range(1, num + 1))

    # lee el tiempo de toma de la imagen
    arch = archivo.split("_", 2)
    tiempo = time.strptime(arch[0] + arch[1], "%Y%m%d%H%M%S")

    # return centros de masa y tiempo de foto
    return center_of_mass, time.mktime(tiempo)

def resetMosaico():
    'Reset images output/mosaico_*.png with lib/img/sun_*.png'

    img = misc.imread ("lib/img/sun_512.png")
    misc.imsave("output/mosaico_512.png", img)

    img = misc.imread ("lib/img/sun_1024.png")
    misc.imsave("output/mosaico_1024.png", img)

    img = misc.imread ("lib/img/sun_2048.png")
    misc.imsave("output/mosaico_2048.png", img)

    img = misc.imread ("lib/img/sun_3072.png")
    misc.imsave("output/mosaico_3072.png", img)

    img = misc.imread ("lib/img/sun_4096.png")
    misc.imsave("output/mosaico_4096.png", img)

# crea lista con nombres de archivos


def getCM_X(center_of_mass, n):
    return center_of_mass[0][n][1]

def getCM_Y(center_of_mass, n):
    return center_of_mass[0][n][0]

def getCM_T(center_of_mass, n):
    return center_of_mass[1]

def getCM_TXY(center_of_mass, n):
    return center_of_mass[1], center_of_mass[0][n][1], center_of_mass[0][n][0]


def getCenterofMassesofImage():
    #lee la lista de archivos
    archivos = ls("img/")

    # mosaico_~.png en blanco
    resetMosaico()

    # Los parametros recomendados son para imagenes de 4096
    # Procesa imagenes tipo *.jpg
    centers_of_masses = {}

    index = 0
    for archivo in archivos:
        if archivo[-4:] == ".jpg":
            centers_of_masses[index] = getCMFromImage(archivo)
            #print "Procesada: " + archivo
            #print center_of_mass[index]
            index = index + 1

    return centers_of_masses


def getKey2(item):
    return item[2]

def getKey3(item):
    return item[3]

def get_ve_com(point, next_points):

    res = []

    for next_point in next_points:
        #revisando xpos
        if next_point[X] > point[X] + DX_MIN: # El +DX_MIN asegura que la mancha si se mueva
            if next_point[X] < point[X] + XERR:
                #revisando ypos
                if next_point[Y] > point[Y] - YERR:
                    if next_point[Y] < point[Y] + YERR:
                        val = next_point[0], next_point[1], abs(next_point[Y] - point[Y]), abs(next_point[X] - point[X])
                        res.append(val)

    #primero ordenar
    res.sort(cmp=None, key=getKey3, reverse=False)
    res.sort(cmp=None, key=getKey2, reverse=False)

    return res

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
    ve_coms.append(temp)

    return ve_coms


comsoi = getCenterofMassesofImage()
center = getCenter(comsoi)

ve_comsoi = {}

for i in range(len(comsoi) - 1):
    ve_comsoi[i] = get_ve_comsoi(comsoi[i], comsoi[i + 1])

print comsoi
print ""
print ve_comsoi