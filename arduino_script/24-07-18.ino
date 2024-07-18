byte pinDrink = 2;
byte pinFlapup = 7;
byte pinFlapdown = 8;

int timeFlapup = 1000;
unsigned long endtimeFlapup = 0;

int timeFlapdown = 1000;
unsigned long endtimeFlapdown = 0;

byte ser1 = 0;

void setup() {
  pinMode(pinDrink, OUTPUT);
  pinMode(pinFlapup, OUTPUT);
  pinMode(pinFlapdown, OUTPUT);
  Serial.begin(9600);
}
void loop() {

  if(Serial.available() > 0){
        delay(3);
    command = Serial.read();

    /*
        --------------- COMMANDS ---------------
        1: turn on the drinker
        2: turn off the drinker
        3: raise the flap
        4: lower the flap
        ----------------------------------------
     */


    switch(command){
      case 1:
        digitalWrite(pinDrink,HIGH);
        break;
      case 2:
        digitalWrite(pinDrink,LOW);
        break;
      case 3:
        endtimeFlapup = millis() + timeFlapup;
        digitalWrite(pinFlapup,HIGH);
        break;
      case 4:
        endtimeFlapdown = millis() + timeFlapdown;
        digitalWrite(pinFlapdown,HIGH);
        break;
    }

  if (endtimeFlapup && endtimeFlapup < millis()){
    digitalWrite(pinFlapup,LOW);
    endtimeFlapup = 0;
  }

  if (endtimeFlapdown && endtimeFlapdown < millis()){
    digitalWrite(pinFlapdown,LOW);
    endtimeFlapdown = 0;
  }
 }
}
