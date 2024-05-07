//Настроечные переменные
  //поилка
byte Drink = 1; //код сигнала по com-порту.
byte pinDrink = 2; //pin для включения устройства
int timeDrink = 3000; //длительность сигнала
unsigned long endtimeDrink = 0; //расчётное время выключения поилки

  //заслонка вверх
byte Flapup = 2; //код сигнала по com-порту.
byte pinFlapup = 3; //pin для включения устройства
int timeFlapup = 1000; //длительность сигнала вверх на заслонку 
unsigned long endtimeFlapup = 0; //расчётный момент выключения устройства

  //заслонка вниз
byte Flapdown = 4; //код сигнала по com-порту.
byte pinFlapdown = 4; //pin включения устройства
int timeFlapdown = 1000; //длительность сигнала
unsigned long endtimeFlapdown = 0; //расчётный момент выключения устройства

  //блокировка левого планшета
byte Blockleft = 8; //код сигнала по com-порту.
byte pinBlockleft = 5; //pin для ввключения устройства
int timeBlockleft = 3000; //длительность сигнала
unsigned long endtimeBlockleft = 0; //расчётный момент выключения устройства

  //блокировка правого планшета
byte Blockright = 16; //код сигнала по com-порту.
byte pinBlockright = 6; //pin для ввключения устройства
int timeBlockright = 3000; //длительность сигнала
unsigned long endtimeBlockright = 0; //расчётный момент выключения устройства

  //дополнительные переменные
byte ser = 0; // переменная для хранения числа из com-port'а

void setup() {
  pinMode(pinDrink, OUTPUT);
  pinMode(pinFlapup, OUTPUT);
  pinMode(pinFlapdown, OUTPUT);
  pinMode(pinBlockleft, OUTPUT);
  pinMode(pinBlockright, OUTPUT);
  Serial.begin(9600);
 
}
void loop() {
  if(Serial.available() > 0){ // если пришёл сигнал
  ser = Serial.read();
  switch(ser){
    case 1:
      Serial.println("case 1");
      endtimeDrink = millis() + timeDrink;
      digitalWrite(pinDrink,HIGH);
      break;
    case 2:
      Serial.println("case 2");
      endtimeFlapup = millis() + timeFlapup;
      digitalWrite(pinFlapup,HIGH);
      break;     
    case 4:
      Serial.println("case 4");
      endtimeFlapdown = millis() + timeFlapdown;
      digitalWrite(pinFlapdown,HIGH);
      break;     
    case 8:
      Serial.println("case 8");
      endtimeBlockleft = millis() + timeBlockleft;
      digitalWrite(pinBlockleft,HIGH);
      break;
    case 16:
      Serial.println("case 16");
      endtimeBlockright = millis() + timeBlockright;
      digitalWrite(pinBlockright,HIGH);
      break;
  }
  }
  ser = 0;
  
// выключить устройство
  if ((endtimeDrink > 0)&&(endtimeDrink < millis())){
    digitalWrite(pinDrink,LOW);
    endtimeDrink = 0;    
  };
  if ((endtimeFlapup > 0)&&(endtimeFlapup < millis())){
    digitalWrite(pinFlapup,LOW);
    endtimeFlapup = 0;    
  };
  if ((endtimeFlapdown > 0)&&(endtimeFlapdown < millis())){
    digitalWrite(pinFlapdown,LOW);
    endtimeFlapdown = 0;    
  };
  if ((endtimeBlockleft > 0)&&(endtimeBlockleft < millis())){
    digitalWrite(pinBlockleft,LOW);
    endtimeBlockleft = 0;    
  };
  if ((endtimeBlockright > 0)&&(endtimeBlockright< millis())){
    digitalWrite(pinBlockright,LOW);
    endtimeBlockright = 0;    
  };
}

