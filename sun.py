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
from pylab import *
from matplotlib.ticker import FormatStrFormatter

def mainSun(comsois, RESOLUCION):

    # Haya el centro del sol en pixeles en base a un promedio del centro de todas las imagenes
    # print sun.getCenter(comsois)
    center = sun.getCenterFromCleanFile("20140701_001500_4096_HMIIF_CLEAN.jpg")

    print "Obteniendo relaciones de seguimiento entre manchas"
    # Calcula valores esperados para las manchas de todas las imagenes
    ve_comsois = sun.get_ve_comsois(comsois)


    print "Procedimiento exitoso."

    # Guarda grafico de seguimiento de manchas en archivo
    print "Dibujando seguimiento de manchas en: output/mosaico_" + str(RESOLUCION) + ".png ..."
    sun.saveMosaico(ve_comsois, RESOLUCION)
    print "Se ha almacenado una imagen del seguimiento de las manchas en: output/mosaico_" + str(RESOLUCION) + ".png"
    print ""

    y, x, sin_x_2 = sun.getPlotValuesFromComsois(comsois, ve_comsois, center)

    print "Realizando regresión polinomica para los datos obtenidos ..."
    # Retorna ax^2+bx+c -> (a, b, c)
    coeffs = np.polyfit(sin_x_2, y, 2, rcond=None, full=False, w=None, cov=False)

    w0, b0, a0 = coeffs[2], coeffs[1] / coeffs[2], coeffs[0] / coeffs[2]
    equ = r'''$w = %(w0)s \cdot (1  + %(b0)s \cdot sin(\theta)^2  + %(a0)s \cdot sin(\theta)^4)$'''
    equ = equ % {'w0': sun.double2latex(w0), 'b0': sun.decimal2latex(b0), 'a0': sun.decimal2latex(a0)}

    print ""
    print "Equación obtenida en formato latex: " + equ

    x_order = []
    max_x = max(x)
    min_x = min(x)
    for i in range(100):
        x_order.append(min_x + i * (max_x - min_x) / 100)

    print "El valor mínimo encontrado para el ángulo theta es: " + str(min_x * 180 / math.pi) + " grados"
    print "El valor máximo encontrado para el ángulo theta es: " + str(max_x * 180 / math.pi) + " grados"

    # create a polynomial using coefficients
    f = np.poly1d(coeffs)

    y_est = f(x_order)

    w_est = np.array(y_est)
    t_est = 2 * math.pi / w_est / 3600 / 24  # dias

    print "La velocidad angular mínima calculada es: " + str(min(y))
    print "La velocidad angular máxima calculada es: " + str(max(y))

    x_est = np.array(x_order)
    x_est = x_est / math.pi * 180  # grados

    nx = np.array(x)
    nx = nx / math.pi * 180  # grados

    # create plot
    xFormatter = FormatStrFormatter('%.0f')
    yFormatter = FormatStrFormatter('%.0e')

    ax = subplot(111)
    plt.plot(nx, y, '.', label='original data', markersize=5)
    plt.plot(x_est, y_est, 'o-', label='estimate', markersize=1)
    ax.xaxis.set_major_formatter(xFormatter)
    ax.yaxis.set_major_formatter(yFormatter)
    xlabel(r'$\theta/[grados]$')
    ylabel(r'$\omega/[rad/s]$')
    title(u"Regresión polinomica de los datos")
    plt.grid()
    savefig('output/comparacion.png')
    plt.show()

    xFormatter = FormatStrFormatter('%.0f')
    yFormatter = FormatStrFormatter('%.2f')
    ax1 = subplot(111)
    plt.plot(x_est, t_est, 'o-', label='estimate', markersize=1)
    ax1.xaxis.set_major_formatter(xFormatter)
    ax1.yaxis.set_major_formatter(yFormatter)
    xlabel(r'$\theta/[grados]$')
    ylabel(r"$\tau$" + u"/[días]")
    title(u'Periodo estimado de rotación')
    plt.grid()
    savefig('output/periodo.png')
    plt.show()

    xFormatter = FormatStrFormatter('%.0f')
    yFormatter = FormatStrFormatter('%.2e')
    ax2 = subplot(111)
    plt.plot(x_est, y_est, 'o-', label='estimate', markersize=1)
    ax2.xaxis.set_major_formatter(xFormatter)
    ax2.yaxis.set_major_formatter(yFormatter)
    xlabel(r'$\theta/[grados]$')
    ylabel(r'$\omega/[rad/s]$')
    title('Velocidad angular estimada')
    plt.grid()
    savefig('output/regresion.png')
    plt.show()

    print ""
    print "Se han almacenado los resultados en:"
    print "\toutput/comparacion.png"
    print "\toutput/regresion.png"
    print "\toutput/periodo.png"


# Get center of masses of images and resolution
# Si se especifica en la linea de comandos entonces no procesara las imagenes
if len(sys.argv) == 2:
    if sys.argv[1] == "-l":
        print "Cargando información de las manchas desde archivo output/datos.dat"
        comsois, RESOLUCION = sun.load_data()
        mainSun(comsois, RESOLUCION)
    elif sys.argv[1] == "512" or sys.argv[1] == "1024" or sys.argv[1] == "2048" or sys.argv[1] == "3072" or sys.argv[1] == "4096":
        RESOLUCION = int(sys.argv[1])
        print "Calculando centros de masa de las manchas en las imagenes ..."
        comsois = sun.getCenterofMassesofImages()
        datos = comsois, RESOLUCION
        sun.save_data(datos)
        print "Procedimiento exitoso. Se ha creado el archivo output/datos.dat"
        print ""
        print "python sun.py [[RESOLUCION] [-l]]"
        print "Use opción '-l' para cargar datos ya procesados."
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

