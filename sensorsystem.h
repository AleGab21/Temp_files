enum sensortype {TEMPERATUR, FUKTIGHET, TRYKK, ROYK};
enum sensortilstand {AV, AKTIV, DVALE, ALARM};
typedef struct {
  unsigned id;
  unsigned adresse;
  unsigned etasje;
  enum sensortype type;
  enum sensortilstand tilstand;
  unsigned verdi;
  float v_batt;
  float v_nom;
  float T_s;
  char kalibrert[10];
} sensor;