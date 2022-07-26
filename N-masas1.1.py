import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import sympy

# Autor: Marcos Sidoruk

################################
######INSTRUCCIONES DE USO######
################################

# Este programa simula un problema de N masas acopladas por resortes a las que se les permite moverse longitudinalmente
# Las masas de los extremos estan acopladas a puntos fijos por resortes, con lo que el sistema contara de N + 1 resortes
# El usuario puede cambiar el input del programa a gusto, esto lo hara cambiando las constantes en mayuscula que se encuentran abajo
# los parametros que el usuario puede cambiar son la cantdidad de masas, los valores de cada masa, los valores de cada constante elastica
# y las condiciones iniciales asi como ciertos parametros no-fisicos relacionados a la computacion de la simulacion
# el usuario puede elegir intoducir las condiciones iniciales de dos maneras: a modo de condiciones iniciales "ordinarias", es decir
# velocidades y posiciones, o a modo de amplitudes y fases de los modos iniciales. Es importante que los parametros sean consistentes entre si
# ( no puede haber 5 masas y 3 valores dados para las mismas ) en caso contrario el programa escribira un texto detallando el error y se detendra
# el programa se puede configurar para que muestre la animacion directamente o lo guarde en un gif, para el gif usa PillowWriter, 
# si tienen otro writer pueden seleccionarlo cambiando una constante. para animaciones que son muy largas y/o cuentan con muchos grados de libertad
# se recomienda guardar la animacion en gif por cuestiones de rendimiento, a continuacion una tabla de testeos que realize.

# numero de G/L # duracion # fps # tiempo de computo # memoria utilizada #
#---------------#----------#-----#-------------------#-------------------#
#     40        #   30     #  30 #      15-20min     #      1.2 GB       #
#     10        #   30     #  30 #         40s       #      1.2 GB       #
#     10        #   20     #  30 #         25s       #      873 MB       #
##########################################################################
# -> Aparentemente los gls no afectan el uso de memoria, si el tiempo de computo

# nota: usar valores pequenos(con respecto a L y YLIM) para las amplitudes de los modos normales, valores grandes pueden resultar en movimientos que salen de la pantalla
# nota: me dio fiaca hacer la parte de las velocidades en las condiciones iniciales, asi que el programa solo toma desplazamientos. el que la tenga mas clara con sympy que lo haga si quiere.
# nota: no se por que, google collab tiene problemas con la funcion FuncAnimation() de matplotlib, van a tener que ejecutar esto en sus compus


## descripcion del sistema ##

CANTIDAD_MASAS = 40                                            # cantidad de masas en el sistema, cantidad de g.l
VECTOR_MASAS = np.array( [ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 ] )                  # empezando por la masa de la izq, los valores de las masas[kg]
VECTOR_K = np.array( [ 100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100 ] )       # empezando por la izq, los valores de las constantes elasticas[kg/s2] (recordar, hay CANTIDAD_MASAS+1 resortes)
L = 10                                                         # longitud del sistema

## parametros fisicos ##

AMPLITUD_MODOS = np.array( [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0 ] )     # amplitud de los modos iniciales[m]
FASES_MODOS = np.array( [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0  ] )       # fases de los modos iniciales[rad]
INPUT_MODOS = True                          # si esta variable es TRUE, el programa toma como imput las amplitudes y fases de los modos normales e ignora lo de abajo, si es FALSE, al revez

DESP_INICIALES = sympy.Matrix( [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0  ] )             # desplazamientos iniciales[m], empezando por la masa de la izq
V_INICIALES = np.array( []  )                # desactivado!!!

## parametros de la simulacion ##
# cuidado! elejir una duracion y FPS muy altos puede llevar a que el programa tarde mucho y potencialmente a que agote
# toda la memoria de tu computadora ( los memory leaks no son mios, la culpa es de matplotlib y python )

FPS = 25                                    # cuadros por segundo de la simulacion
DURATION = 15                               # duracion de la simulacion
OUT_NAME = 'N-masas.gif'                    # Nombre del archivo de output (.gif)
YLIM = 5                                   # distancia entre el eje y y el limite superior/inferior de la pantalla
WRITER = 'PillowWriter'                     # programa utilizado para crear el gif
SAVE = True                                 # si es true se crea un gif, sino se muestra la animacion directamente

## NO TOCAR!! ##

omegas = []
aut_vecs = []

eqsx = []
eqsy = []

fig = plt.figure()
ax = plt.axes( xlim = (0,L), ylim = ( -YLIM, YLIM ) )
puntitos, = plt.plot( [], [], 'ko' )


# esta funcion verifica que el input dado sea consistente
def in_check():

    if np.size( VECTOR_MASAS ) != CANTIDAD_MASAS:

        print("ERROR: VECTOR_MASAS debe contener tantos elementos como indicados por CANTIDAD_MASAS")
        quit()

    if np.size( VECTOR_K ) != CANTIDAD_MASAS + 1:

        print("ERROR: VECTOR_K debe contener exactamente CANTIDAD_MASAS + 1 elementos")
        quit()

    if INPUT_MODOS == True:

        if np.size(FASES_MODOS) != np.size(AMPLITUD_MODOS) or np.size(FASES_MODOS) != CANTIDAD_MASAS:

            print( "ERROR: se especifico el tipo de input a amplitudes y fases de los modos normales, los vectores AMPLITUD_MODOS y FASES_MODOS deben contener tantos elementos como indicados por CANTIDAD_MASAS" )
            quit()

    elif np.size(DESP_INICIALES) != CANTIDAD_MASAS:

        print( "ERROR: se especifico el tipo de input a condiciones iniciales del sistema, los vector DESP_INICIALES debe contener tantos elementos como indicados por CANTIDAD_MASAS" )
        quit()

# esta funcion escribe las ecuaciones de newton, es decir, encuentra la matriz asociada al sistema
def create_system_matrix():
    
    matriz_aux = []
    for i in range( CANTIDAD_MASAS ):
        
        matriz_fila = []
        for j in range( CANTIDAD_MASAS ):

            if j == i - 1:

                matriz_fila.append( VECTOR_K[i]/VECTOR_MASAS[i] )

            elif j == i:

                matriz_fila.append( -(VECTOR_K[i]+VECTOR_K[i+1])/VECTOR_MASAS[i] )

            elif j == i+1:

                matriz_fila.append( VECTOR_K[i+1]/VECTOR_MASAS[i] )

            else:

                matriz_fila.append(0)

        matriz_aux.append( matriz_fila )
        
    return sympy.Matrix( matriz_aux )

# esta funcion tan solo separa la matriz de cambio de base dada por sympy en los autovectores
def obtener_autovectores( m_base ):
        
    global aut_vecs

    aut_vec_list = []
    for i in range( CANTIDAD_MASAS ):
        
        aux = []
        for j in range( CANTIDAD_MASAS ):
             
            aux.append( float(m_base.col(i)[j]) )
        
        aut_vec_list.append( np.array(aux) )

    aut_vecs = aut_vec_list
        

# esta funcion tan solo crea una lista con los valores de la diagonal de la matriz dada por simpy
def obtener_autovalores( m_diag ):

    global omegas
    
    for i in range( CANTIDAD_MASAS ):

        omegas.append( np.sqrt(float( -m_diag.row(i)[i] ) ) )

# esta funcion hace poco, pero matplotlib la necesita para animar.
def init_animation():
    
    global eqsx
    global eqsy
        
    puntitos, = plt.plot( [], [], 'ko')

    return puntitos,


# en esta funcion esta escrita la solucion general en funcion de los autovectores, autovalores, y el tiempo, luego se la podemos pasar a matplotlib
def animar( frame ):
    
    t = frame/FPS

    eqs_aux = np.array(eqsx)
    
    x = np.array( eqsy )
    for i in range( CANTIDAD_MASAS ):

        x = np.add( x, aut_vecs[i]*AMPLITUD_MODOS[i]*np.cos( omegas[i]*t + FASES_MODOS[i] ) )
    
    x = np.add( x, np.array(eqsy) )

    puntitos.set_data( eqsx, x.tolist() )

    return puntitos,

def main(): 
    
    global AMPLITUD_MODOS
    global FASES_MODOS
    global omegas
    global aut_vecs
    global eqsx
    global eqsy
    
    #chequear imput
    in_check()

    #escribir newton
    matriz_newton = create_system_matrix()
    
    #diagonalizar
    m_base, m_diag = matriz_newton.diagonalize()

    # conseguir los autovectores y autovalores
    obtener_autovectores( m_base )
    obtener_autovalores( m_diag )
    
    # ahora si el input en funcion de los modos normales no es dado, hay que calcularlo.
    if INPUT_MODOS == False:
        
        AMPLITUD_MODOS = []
        FASES_MODOS = []

        amplitudes_list = []
        fases_list = []

        amplitud_modos_aux = m_base.inv()* (DESP_INICIALES)

        for i in amplitud_modos_aux:

            amplitudes_list.append( i )
            fases_list.append(0)

        AMPLITUD_MODOS = np.array( amplitudes_list )
        FASES_MODOS = np.array( fases_list )
        

    # luego podemos animar


    for i in range( CANTIDAD_MASAS ):

        eqsx.append( (i+1)*L/(CANTIDAD_MASAS+1) )
        eqsy.append( 0 )
    
    for i in eqsx:

        plt.plot( [ i, i ], [ -YLIM, YLIM ], lw = 0.1, color = "red" )

    animation = anim.FuncAnimation( fig, animar, init_func = init_animation, interval = 1000/FPS, frames = DURATION*FPS, blit = True )

    if SAVE == True: animation.save( OUT_NAME, writer=WRITER, fps=FPS)
    else: plt.show()
    


main()
