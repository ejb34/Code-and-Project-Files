             
#include <LiquidCrystal.h>

#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#ifndef PSTR
 #define PSTR 
#endif


//LCD INPUT INITIALIZATION
  const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
  const int button = 8;

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

//LED MATRIX 32x8 SETUP
Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(32, 8, 6,
  NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);

     


//ANALOG JOYSTICK INITIALIZATION
#define joyX A0
#define joyY A1

const String none = "NONE";

//COLORS
  const String red = "RED";
  const String green = "GREEN";
  const String blue = "BLUE";
  const String purple = "PURPLE";
  const String orange = "ORANGE";
  const String yellow = "YELLOW";
  
//SHAPES
  const String Square = "SQUARE";
  const String triangle = "TRIANGLE";
  const String circle = "CIRCLE";
  const String rhombus = "RHOMBUS";
  const String rectangle = "RECTANGLE";
  const String octagon = "OCTAGON";
  
//CHANGING VARIABLES
  int selectionCount = 0;
  int choice = 0;
  String selectedColor = none;
  String selectedShape = none;
  uint16_t ledColor;
  
void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);
  pinMode(10, INPUT_PULLUP);
  lcd.noBlink();

  matrix.begin();
  
  matrix.setBrightness(3);
  
}

void loop() {
  int xValue = analogRead(joyX);
  int yValue = analogRead(joyY);
  String x;
  String y;

//STICK DIRECTION DETECTION VIA STRING

 //LEFTRIGHT
  if (xValue < 450) {
    x = "LEFT";
  }

  if (xValue > 650) {
    x = "RIGHT";
  }

 //UPDOWN
  if (yValue > 650) {
    y = "DOWN";
  }

  if (yValue < 450) {
    y = "UP";
  }
  
  //Y NEUTRAL CHECK
    if (yValue > 513 && yValue < 516) {
      y = "";
    }

//MENU DEFAULT
  String nextSelection;
  String top = "SELECT COLOR:";

//DIRECTIONAL STRING SELECTION
  if (x == "RIGHT") {
    lcd.clear();
    choice = 1;
  }
  
  if (x == "LEFT") {
    lcd.clear();
    choice = 0;
  }
  
  if (y == "UP") {
    lcd.clear();
    selectionCount = selectionCount - 1;
  }
  
  if (y == "DOWN") {
    lcd.clear();
    selectionCount = selectionCount + 1;
  }

  if (selectionCount == 7) {
    selectionCount = 0;
  }

  if (selectionCount == -1) {
    selectionCount = 6;
  }

//COLOR MENU
  if (choice == 0) {

    top = "SELECT COLOR:";

    if (selectionCount == 0) {
      nextSelection = red;
    }
    if (selectionCount == 1) {
      nextSelection = blue;
    }
    if (selectionCount == 2) {
      nextSelection = green;
    }
    if (selectionCount == 3) {
      nextSelection = yellow;
    }
    if (selectionCount == 4) {
      nextSelection = orange;
    }
    if (selectionCount == 5) {
      nextSelection = purple;
    }
    if (selectionCount == 6) {
      nextSelection = none;
    }
    
  }
  
//SHAPE MENU
  if (choice == 1) {

    top = "SELECT SHAPE:";

    if (selectionCount == 0) {
      nextSelection = Square;
    }
    
    if (selectionCount == 1) {
      nextSelection = triangle;
    }
    
    if (selectionCount == 2) {
      nextSelection = circle;
    }
    
    if (selectionCount == 3) {
      nextSelection = rhombus;
    }
    
    if (selectionCount == 4) {
      nextSelection = rectangle;
    }
    
    if (selectionCount == 5) {
      nextSelection = octagon;
    }
    if (selectionCount == 6) {
      nextSelection = none;
    }
    
  }

//MENU PRINT TO LCD
  String bottom = nextSelection;

  lcd.setCursor(2, 0);
  lcd.print(top);
  lcd.setCursor(3, 1);
  lcd.print("[" + bottom + "]");

//COLOR & SHAPE SELECTION USING JOYSTICK SWITCH
  if (digitalRead(10) == LOW) {
    String selectionString;

    if (choice == 0) {
      selectedColor = nextSelection;
      selectionString = nextSelection;
    }

    if (choice == 1) {
      selectedShape = nextSelection;
      selectionString = nextSelection;
    }

  //SELECTION POPUP SCREEN
    lcd.clear();

    lcd.setCursor(2, 0);
    lcd.print("\"" + selectionString + "\"");
    lcd.setCursor(3, 1);
    lcd.print("SELECTED") ;

    delay(2000);
    lcd.clear();
  }

//LED MATRIX OUTPUT
 if (selectedColor == red){\
   matrix.clear();
  ledColor = matrix.Color(255, 0,  0);
  
 }

  if (selectedColor == green){
    matrix.clear();
  ledColor = matrix.Color(0, 255, 0);
  
 }

  if (selectedColor == blue){
    matrix.clear();
  ledColor = matrix.Color(0, 0, 255);
  
 }

  if (selectedColor == purple){
    matrix.clear();
  ledColor = matrix.Color(255, 77, 255);
  
 }

  if (selectedColor == orange){
    matrix.clear();
  ledColor = matrix.Color(255, 177, 0);
  
 }

  if (selectedColor == yellow){
    matrix.clear();
  ledColor = matrix.Color(255, 255, 0);
  
 }

  matrix.fillScreen(0);

  if(selectedShape == none){
    matrix.fillScreen(ledColor);
  }
 
  if(selectedColor == none){
    matrix.fillScreen(0);
  }

  matrix.setCursor(32, 0);

  matrix.show();

//REFRESH
  delay(200);


}
