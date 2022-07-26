# Autor: Marcos Sidoruk

############################################
################ COMO USAR #################
############################################

# El programa simula una cuerda con bordes fijos
# El usuario puede cambiar la descripcion del sistema, las condiciones iniciales, y ciertos parametros relacionados con la simulacion
# Esto se hace cambiando las constantes que se encuentran abajo, y en caso de las condiciones iniciales, el usuario debe escribir dos
# funciones dependientes de la posicion (x) que devuelvan respectivamente las posiciones y las velocidades iniciales de la cuerda en cada punto
# el programa acepta input en forma de o bien condicione iniciales fisicas, o bien amplitudes y fases de los modos normales
# ademas, se puede poner el programa en dos modos: el de crear un gif como output, o el de mostrar el resultado directamente
# para el gif, se requiere tener un programa externo que trabaje con la libreria matplotlib, por default, usa pillow writer, pero esto se puede cambiar.

import matplotlib
matplotlib.use('agg')

import numpy as np
import sympy as sp
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import matplotlib.animation as anim

###### descripcion del sistema #######

L = 30              # longitud de la cuerda [m]
MU = 1            # densidad lineal de la cuerda [kg/m]
T = 100              # tension de la cuerda [N]

###### condiciones iniciales ######

# posicion inicial de la cuerda (psy) en funcion de x, tener en cuenta que el integrador de scipy tiene sus limitaciones, 
# fallara si la funcion aqui abajo es muy rara
def initial_pos(x):
    
    psy = 0

#    if x < L/2:
#        psy = x
#
#    else:
#        psy = -x + L
#
    return psy

# velocidad inicial de la cuerda (psydot) en funcion de x, misma consideracion de arriba
def initial_velocity(x):
   
    psydot = 0

    if x < L/2 + 1 and x > L/2 -1:
        psydot = 10

    return psydot


INPUT_MODOS = False                      # si es TRUE, las condiciones iniciales seran las amplitudes y fases de los modos especificados abajo

# nota: el vector de amplitudes y el vector de fases deben de tener menos elementos que lo especificado en CANTIDAD_MODOS, el programa automaticamente
# inicializa los modos restantes a 0
AMPLITUD_MODOS = [ 0,0,0,0,0,0,0,0,0,0 ]        # amplitudes de los modos normales
FASES_MODOS = []                                # fases de los modos normales

###### parametros de simulacion ######

CANTIDAD_MODOS = 20             # cantidad de modos normales a considerar
X_DIVISIONS = 1000              # cantidad de intervalos de x

FPS = 25                        # cuadros por segundo de la simulacion [s**-1]
DURACION = 10                   # duracion de la simulacion [s]
YLIM = 8                        # distancia desde el equilibrio hasta los limites inf y sup de la pantalla

SAVE = True                     # si es True, se guardara la simulacion en forma de gif
OUT_NAME = "cuerda.gif"         # nombre del archivo de output(.gif) si SAVE = True
WRITER = "PillowWriter"         # nombre del programa usado para crear los gifs

# DONT TOUCH!!!

K = []
OMEGA = []

V = np.sqrt(T/MU)

fig = plt.figure()                                           # crear una figura de matplotlib
ax = plt.axes( xlim = [ 0, L ], ylim = [ -YLIM, YLIM ] )     # define los limites en x e y del grafico
string, = plt.plot( [], [], color = "red" )                  # creamos el objeto "cuerda"(que es un grafico) que vamos a dibujar

X = np.linspace( 0, L, X_DIVISIONS )                         # creamos una lista X que van a ser los puntos sobre los cuales vamos a graficar 


# esta funcion verifica que el input del usuario sea consistente
def check_input():

    if INPUT_MODOS == True:

        if len(AMPLITUD_MODOS) > CANTIDAD_MODOS:
            print("ERROR: Se dieron mas valores para las amplitudes de los modos normales que lo especificado por CANTIDAD_MODOS")
            quit()

        if len(FASES_MODOS) > CANTIDAD_MODOS:
            print("ERROR: Se dieron mas valores para las fases de los modos normales que lo especificado por CANTIDAD_MODOS")
            quit()

    return


# Esta funcion calcula las frecuencias espaciales de los modos normales
def calculate_K():
    
    k = []
    for i in range(CANTIDAD_MODOS):

        k.append( (i+1)*np.pi/L)

    return k

# esta funcion calcula las frecuencias temporales de los modos normales
def calculate_omega( ):
    
    global K

    omega = []
    for i in range(CANTIDAD_MODOS):

        omega.append( K[i]*V )

    return omega

# esta funcion calcula las amplitudes y las fases de los modos normales a travez de metodos de fourier
def fourier( f, g ):
        
    global K
    global OMEGA

    amplitudes = []
    phases = []

    for i in range(CANTIDAD_MODOS):

        integrand1 = lambda x: np.sin( K[i]*x )*initial_pos(x)
        integrand2 = lambda x: np.sin( K[i]*x )*initial_velocity(x)
 
        int1 = (2/L)*integrate.quad( integrand1, 0, L )[0]
        int2 = (2/L)*integrate.quad( integrand2, 0, L )[0]
        
        amplitudes.append( np.sqrt( int1**2 + (int2/OMEGA[i])**2 ) )
        phases.append( -np.arccos( int1/amplitudes[-1] ) )

    return amplitudes, phases

# funcion que hace poco, pero matplotlib la necesita para graficar
def init_animation():
            
        string, = plt.plot( [], [], color = "red" )

        return string,


# esta funcion dice que dibujar en funcion del cuadro en que te encuentres
def animar( frame ):
    
    global K
    global OMEGA
    global AMPLITUD_MODOS
    global FASES_MODOS
    
    t = frame/FPS

    plt.cla()

    y = np.array( np.linspace( 0, 0, len(X) ) )
    for i in range( 0, CANTIDAD_MODOS ):
        
        y_aux = []
        for j in range( len(X) ):

            y_aux.append( AMPLITUD_MODOS[i] * np.sin(K[i]*X[j]) * np.cos( OMEGA[i]*t + FASES_MODOS[i] ) )

        y = y + np.array( y_aux )

    string.set_data( X, y.tolist() )

    return string,


# funcion principal
def main():
    
    global AMPLITUD_MODOS
    global FASES_MODOS
    global K
    global OMEGA
    
    # verificar la coherencia del input
    check_input()

    # calcular las frecuencias espaciales
    K = calculate_K()

    #calcular las frecuencias temporales
    OMEGA = calculate_omega( )

    # si el input es dado en funcion de las condiciones iniciales, hacer fourier
    if INPUT_MODOS == False:
        
        AMPLITUD_MODOS, FASES_MODOS = fourier( initial_pos, initial_velocity )

    else:
        
        # sino, rellenar lo que no ha sido completado en AMPLITUD_MODOS y FASES_MODOS con 0
        while len(AMPLITUD_MODOS) < CANTIDAD_MODOS:
            AMPLITUD_MODOS.append(0)

        while len(FASES_MODOS) < CANTIDAD_MODOS :
            FASES_MODOS.append(0)

    # ahora podemos animar
    animacion = anim.FuncAnimation( fig, animar, init_func = init_animation, interval = 1000/FPS, frames = FPS*DURACION, blit = True )
    
    # guardamos si save = True, mostramos el resultado si no
    if SAVE == True:
        animacion.save( OUT_NAME, writer = WRITER, fps = FPS )
    else:
        plt.show()


main()
