#include<stdio.h>
#include<stdlib.h>
#include<math.h>

#define C 10

typedef double (*field_t)( double[3], double );

typedef struct source_{
	
	double position[3];
	double ang_freq;
	double phase;
	double amplitude;

	double space_freq;	
}SOURCE;

typedef struct screen_{
	
	double size;
	double n_pixels;
	double time_resolution;

	SOURCE *sources;

}SCREEN;

// utilidad, norma de un vector
double vec3_norm( double *v ){

	return sqrt( v[0]*v[0] + v[1]*v[1] + v[2]*v[2] );
}

void vec3_sub( double *v, double *w, double *out ){

	for( int i = 0; i < 3; i++ )
		out[i] = v[i] - w[i];
}

void vec3_copy( double *v, double *out ){

	for( int i = 0; i < 3; i++ )
		out[i] = v[i];
}

// el final del array sources debe estar indicado por un puntero nulo sino el programa va a segfaultear
// esta funcion cambia a x, NO USAR ESA VARIABLE DESPUES DE LLAMAR A ESTA FUNCION
double set_intensity( double *x, double t, SOURCE *sources ){
	
	double field_val = 0;
	for( int i = 0; sources + i != NULL; i++ ){
		
		double *position = sources[i].position;
		double ang_freq = sources[i].ang_freq;
		double phase = sources[i].phase;
		double amplitude = sources[i].amplitude;
		double spatial_freq = sources[i].space_freq;
		
		vec3_sub( x, position, x );

		double r = vec3_norm( x );
		
		if( r == 0 ){
			continue;
		}
		field_val += amplitude * cos( ang_freq * t + spatial_freq * r + phase )/r;
	}
	return field_val * field_val;
}

// si el integrando es muy grande puede empezar a haber problemas de overflow / perdida de precision por el modo en
// el que esta manejado la variable result, esto es asi por cuestiones de eficiencia que bien podrian ser
// despreciables, cambiar esto si se observan problemas.
double integrate( double (*f)( double*, double, SOURCE* ), double t0, double t1, double step, double *x, SOURCE* sources){
	
	double result = 0;
	double t;
	for( int i = 0; (t = i*step + t0) < t1; i++ ){
		
		result += f( x, t, sources );
	}
	result *= step;
	return result;
}

SOURCE create_source( double *position, double ang_freq, double phase, double amplitude ){

	SOURCE result;
	
	vec3_copy( position, result.position );

	result.ang_freq = ang_freq;
	result.phase = phase;
	result.amplitude = amplitude;

	result.space_freq = ang_freq/C;

	return result;
}

void unit_vec_from_angle( double theta, double *v ){

    v[0] = cos( theta );
    v[1] = sin( theta );
    v[2] = 0;
}

double **michaelson_ang( double alpha, double *dist, double ang_freq, SCREEN screen ){
    
    double unit_vec[3];
    unit_vec_from_angle( alpha, unit_vec );

	double **result = malloc( screen.n_pixels * sizeof(double*) );
	for( int i = 0; i < screen.n_pixels; i++ )
		result[i] = malloc( screen.n_pixels * sizeof(double) );
	
	SOURCE *sources = malloc( 100 * sizeof(SOURCE) );
	for( int i = 0; dist[i] != 0 && i < 100; i++ ){
	    
        vec3_copy( unit_vec, sources[i].position );
        vec3_scal( dist[i], sources[i].position );
        sources[i].ang_freq = ang_freq;
        sources[i].phase = 0;
        sources[i].amplitude = 1;
    }
    

}

int main(){
	return 0;
}
