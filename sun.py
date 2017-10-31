# -*- coding: utf-8 -*-
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

from lib import libsun as sun
import sys

# Resolucion
RESOLUCION = ""

# Centro de las imagenes del sol
center = 0, 0

# Diccionario para guardar los valores de cada mancha
comsois = {}

# Diccionario para guardar los siguientes valores esperados para cada mancha
ve_comsois = {}

def mainSun():

    # Haya el centro del sol en pixeles en base a un promedio del centro de todas las imagenes
    center = sun.getCenter(comsois)

    # Calcula valores esperados para las manchas de todas las imagenes
    ve_comsois = sun.get_ve_comsois(comsois)

    # Guarda grafico de seguimiento de machas en archivo
    sun.saveMosaico(ve_comsois, RESOLUCION)

    # Procedimiento exitoso
    print "Procedimiento exitoso"

# Get center of masses of images and resolution
# Si se especifica en la linea de comandos entonces no procesara las imagenes
if len(sys.argv) == 2:
    if sys.argv[1] == "-l":
        comsois, RESOLUCION = sun.load_data()
        mainSun()
    elif sys.argv[1] == "512" or sys.argv[1] == "1024" or sys.argv[1] == "2048" or sys.argv[1] == "3072" or sys.argv[1] == "4096":
        RESOLUCION = sys.argv[1]
        comsois = sun.getCenterofMassesofImages()
        datos = comsois, RESOLUCION
        sun.save_data(datos)
        mainSun()
    else:
        print "Argumento invalido. Pruebe:"
        print ""
        print "python sun.py [[RESOLUCION] [-l]]"
        print "Use opción '-l' para cargar datos ya procesados."
else:
    print "Numero de argumentos invalidos. Pruebe:"
    print ""
    print "python sun.py [[RESOLUCION] [-l]]"
    print "Use opción '-l' para cargar datos ya procesados."

