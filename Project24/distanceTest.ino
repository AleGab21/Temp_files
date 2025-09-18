#include <Wire.h>
#include "Adafruit_VL53L1X.h"

#define IRQ_PIN_L 2
#define XSHUT_PIN_L 3

#define IRQ_PIN_M 4
#define XSHUT_PIN_M 5

#define IRQ_PIN_R 6
#define XSHUT_PIN_R 7

static int button = 8;
static int Vibr_L = 9;
static int Vibr_M = 10;
static int Vibr_R = 11;

short int mode = 0;
short int button_state = 0;
short int last_button_state = 0;
short int current_button_state = 0;

static int map_1[4] = {30, 4000, 254, 0};
static int map_2[4] = {30, 4000, 160, 0};
static int map_3[4] = {30, 4000, 80, 0};
int map_val[4] = {0, 0, 0, 0};

Adafruit_VL53L1X vl53_L = Adafruit_VL53L1X(XSHUT_PIN_L, IRQ_PIN_L);
Adafruit_VL53L1X vl53_M = Adafruit_VL53L1X(XSHUT_PIN_M, IRQ_PIN_M);
Adafruit_VL53L1X vl53_R = Adafruit_VL53L1X(XSHUT_PIN_R, IRQ_PIN_R);

void setup() {
  Serial.begin(115200);
  Wire.begin();

  pinMode(Vibr_L, OUTPUT);
  pinMode(Vibr_M, OUTPUT);
  pinMode(Vibr_R, OUTPUT);
  pinMode(button, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);

  while (!Serial)
    delay(10);

  // Initialize Sensors
  if (!vl53_L.begin(0x30, &Wire)) {
    Serial.println(F("Failed to initialize Left Sensor!"));
    while (1)
      delay(10);
  }
  vl53_L.setTimingBudget(50);
  vl53_L.startRanging();

  if (!vl53_M.begin(0x31, &Wire)) {
    Serial.println(F("Failed to initialize Middle Sensor!"));
    while (1)
      delay(10);
  }
  vl53_M.setTimingBudget(50);
  vl53_M.startRanging();

  if (!vl53_R.begin(0x32, &Wire)) {
    Serial.println(F("Failed to initialize Right Sensor!"));
    while (1)
      delay(10);
  }
  vl53_R.setTimingBudget(50);
  vl53_R.startRanging();
}

void Mode_select() {
  if (analogRead(A1) > 300) {
    mode = 0;
  } else if (analogRead(A2) > 300) {
    mode = 1;
  } else if (analogRead(A3) > 300) {
    mode = 2;
  }

  switch (mode) {
    case 0:
      for (int i = 0; i < 4; ++i) {
        map_val[i] = map_1[i];
      }
      break;

    case 1:
      for (int i = 0; i < 4; ++i) {
        map_val[i] = map_2[i];
      }
      break;

    case 2:
      for (int i = 0; i < 4; ++i) {
        map_val[i] = map_3[i];
      }
      break;
  }
}

void Sight_L() {
  if (vl53_L.dataReady()) {
    int16_t distance_L = vl53_L.distance();
    if (distance_L != -1) {
      Serial.print(F("Distance_L: "));
      Serial.print(distance_L);
      Serial.println(" mm");

      int map_distance_L = map(distance_L, map_val[0], map_val[1], map_val[2], map_val[3]);
      analogWrite(Vibr_L, constrain(map_distance_L, 0, 255));
    } else {
      Serial.println(F("Failed to read Left Sensor!"));
    }
    vl53_L.clearInterrupt();
  }
}

void Sight_M() {
  if (vl53_M.dataReady()) {
    int16_t distance_M = vl53_M.distance();
    if (distance_M != -1) {
      Serial.print(F("Distance_M: "));
      Serial.print(distance_M);
      Serial.println(" mm");

      int map_distance_M = map(distance_M, map_val[0], map_val[1], map_val[2], map_val[3]);
      analogWrite(Vibr_M, constrain(map_distance_M, 0, 255));
    } else {
      Serial.println(F("Failed to read Middle Sensor!"));
    }
    vl53_M.clearInterrupt();
  }
}

void Sight_R() {
  if (vl53_R.dataReady()) {
    int16_t distance_R = vl53_R.distance();
    if (distance_R != -1) {
      Serial.print(F("Distance_R: "));
      Serial.print(distance_R);
      Serial.println(" mm");

      int map_distance_R = map(distance_R, map_val[0], map_val[1], map_val[2], map_val[3]);
      analogWrite(Vibr_R, constrain(map_distance_R, 0, 255));
    } else {
      Serial.println(F("Failed to read Right Sensor!"));
    }
    vl53_R.clearInterrupt();
  }
}

void loop() {
  Mode_select();
  Sight_L();
  Sight_M();
  Sight_R();
  delay(100); // Small delay to prevent spamming the I2C bus
}
