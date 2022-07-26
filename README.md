# Otros-Scripts-de-F2
Scripts variados que cree cursando F2

tp_numerico.py:
utilidad de python para simular lo que se veria en una pantalla sensible a ciertas ondas en presencia de fuentes.
contiene dos clases, una que define las fuentes y otra que define la pantalla, con estas dos clases se pueden describir una
amplia gamma de problemas de interferencia. el script es totalmente agnostico con respecto a la naturaleza fisica de las ondas o las unidades.

tp_numerico.c:
version en C del script anterior, ese es muy lento, actualmente sin terminar.

cuerda.py:
simulador de una cuerda ideal perfectamente elastica sin amortiguamiento. para usarlo se debe proveer una implementacion de las funciones
que describen las condiciones iniciales o fijar la cte. INPUT_MODOS a true y dar valores para las amplitudes de los modos normales.

N-masitas1.1.py:
Simulador general de oscilaciones transversales en un sistema de N masitas ligadas a puntos fijos por los extremos.
proveer un array con los valores de las masas y otro con los valores de las ctes. elasticas de los resortes.
luego proveer o bien dos arrays con condiciones iniciales o bien dos arrays con las amplitudes y fases de los modos.
todos los parametros al principio del script se pueden cambiar.
