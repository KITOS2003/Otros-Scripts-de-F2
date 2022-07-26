import numpy as np
import scipy.integrate as si
import matplotlib.pyplot as plt
import seaborn as sb

# este programa fue creado por marcos sidoruk como un trabajo final de fisica 2
#
# el problema a resolver consiste en un interferometro similar al de michaelson
# se pide la distribucion de intensidad en una pantalla ubicada a una cierta distancia
# de dos fuentes que se posicionan una detras de la otra con respecto a la pantalla
# luego se pide la misma distribucion si la pantalla se inclina arbitrariamente
#
# por motivos tecnicos, es mucho mas facil mover las fuentes que la pantalla
# por lo tanto disenaremos el programa tal que la pantalla este fija en el plano xy
# y sean las fuentes las que se muevan para que estas terminen a la inclinacion que el
# usuario desee, ademas el programa contara con grados de libertad
# extra que no son requeridas por el enunciado pero que son faciles de implementar y
# resultan en codigo mas limpio.


# DEFINICIONES:

# el usuario puede cambiar las siguientes:

C = 0.1            # velocidad de las ondas

# nota: la pantalla esta centrada en el 0 y es cuadrada de lado DEF_SCREEN_SIZE
DEF_SCREEN_RES = 10     # factor de conversion pixeles/metro
DEF_SCREEN_SIZE = 20    # en metros
DEF_SCREEN_TIME_RES = 1 # intervalo de tiempo sobre el cual la pantalla promedia la intensidad

# esto es una manera de definir una funcion source() tal que se puedan crear multiples
# instancias cada una con distintos valores para ciertos parametros internos
# primero se crea un objeto de esta clase lo que automaticamente llama a __init__ y
# inicializa los parametros, luego el objeto se puede usar como una funcion gracias al
# metodo __call__
# cada instancia de esta clase representa una fuente puntual.
class source:

    def __init__( self, position: np.ndarray, ang_freq, phase = 0, amplitude = 1, line = False ):
        
        self.position = position
        self.ang_freq = ang_freq
        self.phase = phase
        self.amplitude = amplitude
        self.spacial_ang_freq = self.ang_freq / C
        
        self.line = line
        if line == True:
            self.position = np.append( position[0:1], position[2] )

    def __call__( self, x: np.ndarray, t: float ):
        
        if self.line == True:
            x = np.append( x[0:1], x[2] )

        r = np.linalg.norm(x-self.position)
        t_phase = self.ang_freq * t - self.spacial_ang_freq * r + self.phase
        
        return self.amplitude * np.sin( t_phase )/r

# misma cosa que arriba, solo que esta clase debe inicializarse una sola vez
# define una funcion que retorna el proedio temporal de la intensidad en cada pixel de la pantalla
class init_screen:

    def __init__( self, screen_size, source_list, screen_resolution = DEF_SCREEN_RES, screen_time_res = DEF_SCREEN_TIME_RES ): 
        self.size = screen_size
        self.res = screen_resolution
        self.sources = source_list
        self.time_res = screen_time_res

        # crea grid correspondiente a la pantalla:
        self.num_pixels = self.res * self.size   # n de pixeles en una direccion
        
        sl = self.size/2
        jmp = 1/self.res

        self.screen = np.mgrid[ -sl:sl:jmp, -sl:sl:jmp ]
        self.screen = self.screen.T
    
    def get_intensity( self, x, t ):
        
        field = 0
        for s in self.sources:
            field += s( x, t )

        return field**2

    # obtener la intensidad en todos los pixeles de la pantalla a tiempo t
    def __call__( self, t ):
     
        result = np.zeros( ( self.num_pixels, self.num_pixels ) )

        for i, row in enumerate( self.screen ):
            for j, v in enumerate( row ):
                v = np.append(v,0)                
                pix_int = lambda t0: self.get_intensity( v, t0 )
                result[i][j] = si.quad( pix_int, t, t+self.time_res )[0]/self.time_res

        return result

# utilidad para pasar de polares a cartesianas
def polar_to_cart( r, theta ):

    x = r*np.cos(theta)
    y = r*np.sin(theta)
    return x,y
 
# resuelve el problema del enunciado
def michaelson_angle( alpha, distances: list, ang_freq, screen_size = DEF_SCREEN_SIZE, screen_res = DEF_SCREEN_RES):
    
    source_list = []
    for d in distances:
        z, x = polar_to_cart( d, alpha )
        v = np.array([ x, 0, z ])
        s = source( v, ang_freq)
        source_list.append(s)

    screen = init_screen( screen_size, source_list, screen_resolution = screen_res )
    
    measurement = screen(0)
    max_value = np.amax( measurement )

    sb.set()
    sb.heatmap( measurement, vmin=0, vmax = max_value )
    plt.savefig("michaelson.jpg")

# extra:
def young( d_sources: list, d_screen, ang_freq, screen_size = DEF_SCREEN_SIZE ):
    
    source_list = []
    for d in d_sources:
        source_list.append( source( np.array([ d, 0, d_screen ] ), ang_freq, line = True ) )

    screen = init_screen( screen_size, source_list )

    measurement = screen(0)
    max_val = np.amax( measurement )

    sb.set()
    sb.heatmap( measurement, vmin = 0, vmax = max_val )
    plt.savefig("young.jpg")


#young( [-1, 1], 10, 100 )
michaelson_angle( 0, [2,4], 10 )
