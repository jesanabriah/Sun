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
import math

#===============================================================================
# Valores de configuracion del programa:
#===============================================================================
X, Y, YX, T, NEXT_INDEX = 1, 0, 0, 1, 3
# Valor predeterminado para el error
XERR, DX_MIN, YERR = 6, 1, 2

def mainSun(comsois, RESOLUCION):

    # Haya el centro del sol en pixeles en base a un promedio del centro de todas las imagenes
    # print sun.getCenter(comsois)
    center = sun.getCenterFromCleanFile("20140701_001500_4096_HMIIF_CLEAN.jpg")

    # Calcula valores esperados para las manchas de todas las imagenes
    ve_comsois = sun.get_ve_comsois(comsois)

    # Guarda grafico de seguimiento de manchas en archivo
    # sun.saveMosaico(ve_comsois, RESOLUCION)

    print sun.printTethaPhiOfPoints(comsois, ve_comsois, center)


# Get center of masses of images and resolution
# Si se especifica en la linea de comandos entonces no procesara las imagenes
if len(sys.argv) == 2:
    if sys.argv[1] == "-l":
        comsois, RESOLUCION = sun.load_data()
        mainSun(comsois, RESOLUCION)
    elif sys.argv[1] == "512" or sys.argv[1] == "1024" or sys.argv[1] == "2048" or sys.argv[1] == "3072" or sys.argv[1] == "4096":
        RESOLUCION = int(sys.argv[1])
        comsois = sun.getCenterofMassesofImages()
        datos = comsois, RESOLUCION
        sun.save_data(datos)
        print "Procedimiento exitoso. Se ha creado el archivo output/datos.dat"
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

