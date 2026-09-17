#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

#define TCA9548A_ADDR   0x70
#define MPU_CHANNEL     0

void selectI2CChannel(uint8_t channel) {
  if (channel > 7) return;
  Wire.beginTransmission(TCA9548A_ADDR);
  Wire.write(1 << channel);
  Wire.endTransmission();
}

// ---------- Parametres d'acquisition ----------
#define SAMPLING_FREQ     1000              // Hz vise
#define DURATION_SECONDS  5                 // duree de capture (5 ou 10s)
#define MAX_SAMPLES       (SAMPLING_FREQ * DURATION_SECONDS)

float axBuf[MAX_SAMPLES];
float ayBuf[MAX_SAMPLES];
float azBuf[MAX_SAMPLES];
unsigned long tBuf[MAX_SAMPLES];

const unsigned long samplingPeriodUs = round(1000000.0 / SAMPLING_FREQ);

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(21, 22);
  Wire.setClock(400000);

  selectI2CChannel(MPU_CHANNEL);
  delay(50);

  if (!mpu.begin()) {
    Serial.println("MPU6050 not found");
    while (1) delay(10);
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setFilterBandwidth(MPU6050_BAND_260_HZ);
  mpu.setSampleRateDivisor(0);

  Serial.println("READY");
}

void acquireSamples() {
  unsigned long t0 = micros();
  unsigned long nextSampleTime = t0;

  for (int i = 0; i < MAX_SAMPLES; i++) {
    while (micros() < nextSampleTime) { }
    nextSampleTime += samplingPeriodUs;

    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    tBuf[i] = micros() - t0;
    axBuf[i] = a.acceleration.x;
    ayBuf[i] = a.acceleration.y;
    azBuf[i] = a.acceleration.z;
  }
}

void dumpCSV() {
  Serial.println("BEGIN_CSV");
  Serial.println("index,time_us,ax,ay,az");
  for (int i = 0; i < MAX_SAMPLES; i++) {
    Serial.print(i);
    Serial.print(",");
    Serial.print(tBuf[i]);
    Serial.print(",");
    Serial.print(axBuf[i], 5);
    Serial.print(",");
    Serial.print(ayBuf[i], 5);
    Serial.print(",");
    Serial.println(azBuf[i], 5);
  }
  Serial.println("END_CSV");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'r') {
      Serial.println("ACQUIRING");
      acquireSamples();
      dumpCSV();
      Serial.println("READY");
    }
  }
}