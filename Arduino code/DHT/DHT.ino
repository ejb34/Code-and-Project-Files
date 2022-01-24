
#include <LiquidCrystal.h>
#include <dht.h>

dht DHT;

#define DHT11_PIN 6

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup()
{
  Serial.begin(9600);
  lcd.begin(16, 2);
  
//  Serial.println("DHT TEST PROGRAM ");
//  Serial.print("LIBRARY VERSION: ");
//  Serial.println(DHT_LIB_VERSION);
//  Serial.println();
//  Serial.println("Type,\tstatus,\tHumidity (%),\tTemperature (C)");
}


void loop()
{
  // READ DATA
  Serial.print("");
  int chk = DHT.read11(DHT11_PIN);
  switch (chk)
  {
    case DHTLIB_OK:
    Serial.print("OK, ");
    break;
    case DHTLIB_ERROR_CHECKSUM:
    Serial.print("Checksum error,\t");
    break;
    case DHTLIB_ERROR_TIMEOUT:
    Serial.print("Time out error,\t");
    break;
    case DHTLIB_ERROR_CONNECT:
        Serial.print("Connect error,\t");
        break;
    case DHTLIB_ERROR_ACK_L:
        Serial.print("Ack Low error,\t");
        break;
    case DHTLIB_ERROR_ACK_H:
        Serial.print("Ack High error,\t");
        break;
    default:
    Serial.print("Unknown error,\t");
    break;
  }
  // PRINT DATA
  Serial.print(DHT.humidity, 1);
  Serial.print(", ");
  Serial.println(DHT.temperature, 1);

  //PRINT TO LCD

  lcd.setCursor(1, 0);
  lcd.print("Temp: " + String(DHT.temperature));
  lcd.setCursor(1, 1);
  lcd.print("Hum: " + String(DHT.humidity));

  delay(2000);
}
