/****************************************************************
   Example1_Basics.ino
   ICM 20948 Arduino Library Demo
   Use the default configuration to stream 9-axis IMU data
   Owen Lyke @ SparkFun Electronics
   Original Creation Date: April 17 2019

   Please see License.md for the license information.

   Distributed as-is; no warranty is given.
 ***************************************************************/
#include "ICM_20948.h" // Click here to get the library: http://librarymanager/All#SparkFun_ICM_20948_IMU

//#define USE_SPI       // Uncomment this to use SPI

#define SERIAL_PORT Serial1
#define DEBUG_PORT Serial

//#define SPI_PORT SPI // Your desired SPI port.       Used only when "USE_SPI" is defined
#define CS_PIN 2     // Which pin you connect CS to. Used only when "USE_SPI" is defined

#define WIRE_PORT Wire1 // Your desired Wire port.      Used when "USE_SPI" is not defined
// The value of the last bit of the I2C address.
// On the SparkFun 9DoF IMU breakout the default is 1, and when the ADR jumper is closed the value becomes 0
#define AD0_VAL 1
#define AD0_VAL2 0


ICM_20948_I2C ICM_1;
ICM_20948_I2C ICM_2;

void setup()
{
  ICM_20948_fss_t myFSS;
  myFSS.a = gpm16;
  myFSS.g = dps2000;
  pinMode(LED_BUILTIN, OUTPUT);
  SERIAL_PORT.begin(9600);
  DEBUG_PORT.begin(9600);
  while (!SERIAL_PORT)
  {
  };

  WIRE_PORT.begin();
  WIRE_PORT.setClock(400000);

  //ICM_1.enableDebugging(); // Uncomment this line to enable helpful debug messages on Serial

  bool initialized = false;
  bool initialized2 = false;
  while (!initialized && !initialized2)
  {

    ICM_1.begin(WIRE_PORT, AD0_VAL);
    ICM_2.begin(WIRE_PORT, AD0_VAL2);

    DEBUG_PORT.print(F("Initialization of sensor 1 returned: "));
    DEBUG_PORT.println(ICM_1.statusString());

    DEBUG_PORT.print(F("Initialization of sensor 2 returned: "));
    DEBUG_PORT.println(ICM_2.statusString());

    if (ICM_1.status != ICM_20948_Stat_Ok)
    {
      DEBUG_PORT.println("Bad sensor 1 status trying again...");
      delay(500);
    }
    else
    {
      ICM_1.setFullScale((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), myFSS);
      DEBUG_PORT.print(F("Sensor 1 'setFullScale' returned: "));
      DEBUG_PORT.println(ICM_1.statusString());
      initialized = true;
    }
    if (ICM_2.status != ICM_20948_Stat_Ok)
    {
      DEBUG_PORT.println("Bad sensor 2 status trying again...");
      delay(500);
    }
    else
    {
      ICM_2.setFullScale((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), myFSS);
      DEBUG_PORT.print(F("Sensor 2 'setFullScale' returned: "));
      DEBUG_PORT.println(ICM_2.statusString());
      initialized2 = true;
    }
  }
}

void loop()
{
  int n;
  int t;
  int sensorcount = 1;
  DEBUG_PORT.println("Awaiting device configuration parameters...");
  
  while (1) {
    sensorcount = SERIAL_PORT.parseInt();
    if (sensorcount == 1 || sensorcount == 2) {
      break;
    }
  }
  DEBUG_PORT.print("Got valid sensor selection input...");
  DEBUG_PORT.println(sensorcount);
  
  while (1) {
    t = SERIAL_PORT.parseInt();
    if ((t > 0) && (t < 11)) {
      break;
    }
  }
  DEBUG_PORT.print("Got valid time input...");
  DEBUG_PORT.println(t);

  n = (t * 834) / sensorcount;
  //about 1.2s

  // MAIN

  float buff[(9 * n) + 20];
  unsigned long times[n];
  unsigned long t0 = millis();
  DEBUG_PORT.println("Capturing...");
  digitalWrite(LED_BUILTIN, HIGH);
  switch (sensorcount) {

    //single sensor
    case 1:
      for (int i = 0; i < n; i++) {

        ICM_1.getAGMT();

        buff[(9 * i)    ] = ICM_1.accX();
        buff[(9 * i) + 1] = ICM_1.accY();
        buff[(9 * i) + 2] = ICM_1.accZ();
        buff[(9 * i) + 3] = ICM_1.gyrX();
        buff[(9 * i) + 4] = ICM_1.gyrY();
        buff[(9 * i) + 5] = ICM_1.gyrZ();
        buff[(9 * i) + 6] = ICM_1.magX();
        buff[(9 * i) + 7] = ICM_1.magY();
        buff[(9 * i) + 8] = ICM_1.magZ();

        times[i] = (millis() - t0);

      }
      break;
    //double sensor
    case 2:
      for (int i = 0; i < (n/2); i++) {

        ICM_1.getAGMT();
        ICM_2.getAGMT();
        buff[(9 * i)    ] = (ICM_1.accX() + ICM_2.accZ())/2;
        buff[(9 * i) + 1] = (ICM_1.accY() + ICM_2.accY())/2;
        buff[(9 * i) + 2] = (ICM_1.accZ() + ICM_2.accX())/2;
        buff[(9 * i) + 3] = (ICM_1.gyrX() + ICM_2.gyrZ())/2;
        buff[(9 * i) + 4] = (ICM_1.gyrY() + ICM_2.gyrY())/2;
        buff[(9 * i) + 5] = (ICM_1.gyrZ() + ICM_2.gyrX())/2;
        buff[(9 * i) + 6] = (ICM_1.magX() + ICM_2.magZ())/2;
        buff[(9 * i) + 7] = (ICM_1.magY() + ICM_2.magY())/2;
        buff[(9 * i) + 8] = (ICM_1.magZ() + ICM_2.magX())/2;

        times[i] = (millis() - t0);
      }
      break;
  }
  unsigned long t1 = millis() - t0;
  DEBUG_PORT.print("done! took ");
  DEBUG_PORT.print(t1);
  DEBUG_PORT.println(" ms");


  digitalWrite(LED_BUILTIN, LOW);
  //  while (SERIAL_PORT.available() == 0) {}

  SERIAL_PORT.println("!");
  int p;
  while (1) {
    p = SERIAL_PORT.parseInt();
    if ((p == 1) || (p == 2)) {
      break;
    }
  }
  if (p == 1) {
    for (int i = 0; i < n/sensorcount; i++) {
      SERIAL_PORT.print("<");
      printFormattedFloat((buff[(9 * i)]), 5, 2);
      SERIAL_PORT.print(" , ");
      printFormattedFloat((buff[(9 * i) + 1]) , 5, 2);
      SERIAL_PORT.print(" , ");
      printFormattedFloat((buff[(9 * i) + 2]) , 5, 2);
      SERIAL_PORT.print(" , ");
      printFormattedFloat((buff[(9 * i) + 3]), 5, 2);
      SERIAL_PORT.print(" , ");
      printFormattedFloat((buff[(9 * i) + 4]), 5, 2);
      SERIAL_PORT.print(" , ");
      printFormattedFloat((buff[(9 * i) + 5]), 5, 2);
      SERIAL_PORT.print(" , ");
      printFormattedFloat((buff[(9 * i) + 6]), 5, 2);
      SERIAL_PORT.print(" , ");
      printFormattedFloat((buff[(9 * i) + 7]), 5, 2);
      SERIAL_PORT.print(" , ");
      printFormattedFloat((buff[(9 * i) + 8]), 5, 2);

      SERIAL_PORT.print(" , ");
      SERIAL_PORT.println(times[i]);
      //SERIAL_PORT.println(" >");
    }
    SERIAL_PORT.println(" >");
    //    SERIAL_PORT.print("Capture duration - Time (ms): ");
    //    SERIAL_PORT.print(t1);
  }

  //delay(3000);
  // MAIn
  DEBUG_PORT.println("Done transferring data");
}

void printFormattedFloat(float val, uint8_t leading, uint8_t decimals)
{
  float aval = abs(val);
  if (val < 0)
  {
    SERIAL_PORT.print("-");
  }
  else
  {
    SERIAL_PORT.print(" ");
  }
  for (uint8_t indi = 0; indi < leading; indi++)
  {
    uint32_t tenpow = 0;
    if (indi < (leading - 1))
    {
      tenpow = 1;
    }
    for (uint8_t c = 0; c < (leading - 1 - indi); c++)
    {
      tenpow *= 10;
    }
    if (aval < tenpow)
    {
      SERIAL_PORT.print("0");
    }
    else
    {
      break;
    }
  }
  if (val < 0)
  {
    SERIAL_PORT.print(-val, decimals);
  }
  else
  {
    SERIAL_PORT.print(val, decimals);
  }
}

//void printScaledAGMT(ICM_20948_I2C *sensor)
//{
//    SERIAL_PORT.print("[ ");
//    printFormattedFloat(sensor->accX(), 5, 2);
//    SERIAL_PORT.print(", ");
//    printFormattedFloat(sensor->accY(), 5, 2);
//    SERIAL_PORT.print(", ");
//    printFormattedFloat(sensor->accZ(), 5, 2);
//    SERIAL_PORT.print(" ], [ ");
//    printFormattedFloat(sensor->gyrX(), 5, 2);
//    SERIAL_PORT.print(", ");
//    printFormattedFloat(sensor->gyrY(), 5, 2);
//    SERIAL_PORT.print(", ");
//    printFormattedFloat(sensor->gyrZ(), 5, 2);
//    SERIAL_PORT.print(" ], [ ");
//    printFormattedFloat(sensor->magX(), 5, 2);
//    SERIAL_PORT.print(", ");
//    printFormattedFloat(sensor->magY(), 5, 2);
//    SERIAL_PORT.print(", ");
//    printFormattedFloat(sensor->magZ(), 5, 2);
//  SERIAL_PORT.print(" ]");
//  SERIAL_PORT.println();
//}
