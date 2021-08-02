#include <LiquidCrystal.h>
// The LCD circuit:
// * LCD RS pin to digital pin 12
// * LCD Enable pin to digital pin 11
// * LCD D4 pin to digital pin 5
// * LCD D5 pin to digital pin 4
// * LCD D6 pin to digital pin 6
// * LCD D7 pin to digital pin 7
// * LCD R/W pin to ground
// * 10K resistor:
// * ends to +5V and ground
// * wiper to LCD VO pin (pin 3)
int trigPin=3;
int echoPin=2;
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 6, d7 = 7;
long count;
long duration;
int startDistance;
int distance;
int range = 14;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup(){
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  lcd.begin(16, 2);
    lcd.display();

  Serial.begin (9600);
  delay(1000);
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  startDistance= duration*0.034/2;
  // Prints the distance on the Serial Monitor
  Serial.print("start Distance: ");
  Serial.println(startDistance);

  
}
  
void loop (){

  int minD = startDistance - range;
  int maxD = startDistance + range;
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration*0.034/2;
  // Prints the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.println(distance);
    
  if (distance > maxD || distance < minD) {
    count += 1;
    delay(250);
  }  
    
  lcd.print("distance: ");  

  lcd.print(distance);
  lcd.setCursor(0,2);
  lcd.print("hit: ");  
  lcd.print(count);
  delay(50);  
  lcd.clear();
  
}
