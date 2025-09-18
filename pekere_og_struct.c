//
// sensorsystem.c

#include <stdio.h>
#include "sensorsystem.h"


void init(sensor *s, int N)
{
	unsigned id[] = {1, 2, 3, 4, 5, 6};
	unsigned adresse[] = {200, 201, 202, 203, 204, 205};
	unsigned etasje[] = {1, 2, 3, 3, 1, 2};
	enum sensortype type[] = {ROYK,ROYK, ROYK, TEMPERATUR, ROYK, ROYK};
	enum sensortilstand tilstand[] = {AKTIV, AKTIV, AKTIV, AKTIV, AKTIV, AKTIV};
	unsigned verdi[] = {0, 0, 0, 293, 0};
	float v_batt[] = {0.0, 0.0, 90.0, 90.0, 0.0};
	float v_nom[] = {3.3, 3.3, 3.3, 3.3, 3.3};
	float T_s[] = {60.0, 60.0, 60.0, 60.0, 60.0};
	for (int i = 0; i < N; i++) {
		s[i].id = i+1;
		s[i].tilstand = tilstand[i];
		s[i].etasje = etasje[i];
		s[i].v_nom = v_nom[i];
		s[i].v_batt = v_batt[i];
		s[i].type = type[i];
	}
}

	sensor sensorer[112];
	int N = 6;

  void slaa_av(int i) {
    sensorer[i].tilstand = AV;
  }
  

sensor* sjekk_bat_niv(float bat){
  for (int i= 0; i < N; i++){
    if (sensorer[i].v_batt < bat){
      //printer ut hvilken senorer som er under bat% 
      //printf("sensor %d er under 85\% \n", sensorer[i].id);
    
      //gir alle sensorer og pekere til sensorene som er under gitt prosent
      sensor* a = &sensorer[i];
      printf("Sensor %d med peker %p er under gitt %0.2f \% \n", a ->id, a, bat);
      
      //gir bare første peker til batteri under gitt prosent.
      //return &sensorer[i];
    }
  }
}
  
  void slaa_av_etasje(int etasje) {
    for (int i = 0; i < N; i++) {
        if (sensorer[i].etasje == etasje) {  // Sjekker om sensoren er i riktig etasje
            slaa_av(i);
        }
    }
}
  

void sjekk_royk(sensor *s, int N)
{
	for(int i=0; i<N; i++) {
		if ((s[i].type == ROYK) && (s[i].tilstand == AKTIV))  {
			printf("RC8ykvarsler %d i etasje %d er paa\n", s[i].id, s[i].etasje);
		}
	}
}



int main()
{
	init(sensorer, N);
	
	//printf av alle sensorer som er unde gitt prosent, eller prosent og peker
    sjekk_bat_niv(85);
  
	// bruker return i funskjon for å printe første peker 
	//printf("peker %p \n", sjekk_bat_niv(85));
	
	//slaa_av(2);
	slaa_av_etasje(2);
	sjekk_royk(sensorer, N);
	


	return 0;
}