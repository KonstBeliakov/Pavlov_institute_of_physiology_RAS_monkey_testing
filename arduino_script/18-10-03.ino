//Устройства и их Настроечные переменные
  //поилка
byte Drink = 1; //код сигнала по com-порту. в newUSB установлен, как 1-1
byte pinDrink = 2; //pin для включения устройства
int timeDrink = 1000; //длительность сигнала
unsigned long endtimeDrink = 0; //расчётное время выключения поилки

  //заслонка вверх
byte Flapup = 2; //код сигнала по com-порту. в newUSB Установлен, как 1-2
byte pinFlapup = 7; //pin для включения устройства
int timeFlapup = 1000; //длительность сигнала вверх на заслонку 
unsigned long endtimeFlapup = 0; //расчётный момент выключения устройства

  //заслонка вниз
byte Flapdown = 4; //код сигнала по com-порту. в newUSB Установлен, как 1-3
byte pinFlapdown = 8; //pin включения устройства
int timeFlapdown = 1000; //длительность сигнала
unsigned long endtimeFlapdown = 0; //расчётный момент выключения устройства

  //блокировка левого планшета
byte Blockleft = 8; //код сигнала по com-порту. в newUSB Установлен, как 1-4
byte pinBlockleft = 5; //pin для ввключения устройства
//int timeBlockleft = 120000; //длительность сигнала
//unsigned long endtimeBlockleft = 0; //расчётный момент выключения устройства

  //блокировка правого планшета
byte Blockright = 16; //код сигнала по com-порту. в newUSB Установлен, как 1-5
byte pinBlockright = 6; //pin для ввключения устройства
//int timeBlockright = 120000; //длительность сигнала
//unsigned long endtimeBlockright = 0; //расчётный момент выключения устройства

  //дополнительные переменные
byte ser1 = 0; // переменная для хранения 1-го байта из com-port'а
byte ser2 = 0; // переменная для хранения 2-го байта из com-port'а

void setup() {
  // назначим пины для устройств, как выходные - OUTPUT
  pinMode(pinDrink, OUTPUT);
  pinMode(pinFlapup, OUTPUT);
  pinMode(pinFlapdown, OUTPUT);
  pinMode(pinBlockleft, OUTPUT);
  pinMode(pinBlockright, OUTPUT);
  //открываем com-port
  Serial.begin(9600);
}
void loop() {
  //включение и отключение по сигналу с компьютера
  if(Serial.available() > 0){ // если пришёл сигнал на com-порт, то будем переключать устройство
        delay(3); //пауза необходимая для надёжного считывания com-порта
    ser1 = Serial.read(); // прочитали и запомнили 1-й байт com-порта
    ser2 = Serial.read(); // прочитали и запомнили 2-й байт com-порта
    
    if((ser1&Drink) == Drink) { // если установлен бит Drink и время конца =0, то
      // endtimeDrink = millis() + timeDrink;  // назначили момент выключения поилки
      digitalWrite(pinDrink,HIGH); // включили поилку
      }
   if((ser1&Drink) < Drink) { // если установлен бит Drink и время конца =0, то
      // endtimeDrink = millis() + timeDrink;  // назначили момент выключения поилки
       digitalWrite(pinDrink,LOW); //выключили поилку
      }
    if((ser1&Flapup) == Flapup){ //если установлен бит заслонки вверх, то
      endtimeFlapup = millis() + timeFlapup;
      digitalWrite(pinFlapup,HIGH); // включили заслонку вверх
      }
    if((ser1&Flapdown) == Flapdown){ //если установлен бит заслонки вниз
      endtimeFlapdown = millis() + timeFlapdown; // назначили момент выключения
      digitalWrite(pinFlapdown,HIGH); // включили заслонку вниз
      }
    if((ser1&Blockleft) == Blockleft){ //если установлен бит блокировки левого планшета
      digitalWrite(pinBlockleft,HIGH); // включили блок левого
      }
      else { //если бит выключен, то
        digitalWrite(pinBlockleft,LOW); //выключили блокировку левого планшета
      }
    if((ser1&Blockright) == Blockright){ //если установлен бит блокировки правого планшета
      digitalWrite(pinBlockright,HIGH); // включили блок правого
      }
      else { //если бит выключен, то
        digitalWrite(pinBlockright,LOW); //выключили блокировку левого планшета
      }
 } // конец цикла включения/выключения по сигналу компьютера
 
// выключить устройство по окончанию времени
  //if ((endtimeDrink > 0)&&(endtimeDrink < millis())){ //если текущее время больше момента ввыключения, то
   // digitalWrite(pinDrink,LOW); //выключили поилку
    //endtimeDrink = 0; // обнулили момент выключения
  //};
  // остановим заслонку вверх
  if ((endtimeFlapup > 0)&&(endtimeFlapup < millis())){ //если текущее время больше момента ввыключения
    digitalWrite(pinFlapup,LOW); //выключили
    endtimeFlapup = 0; // обнулили время
  };
  if ((endtimeFlapdown > 0)&&(endtimeFlapdown < millis())){ //если текущее время больше момента ввыключения
    digitalWrite(pinFlapdown,LOW); //выключили
    endtimeFlapdown = 0; // обнулили время
  };
/* (пока) блокировку не снимаем по таймеру
  if ((endtimeBlockleft > 0)&&(endtimeBlockleft < millis())){
    digitalWrite(pinBlockleft,LOW);
    endtimeBlockleft = 0;    
  };
  if ((endtimeBlockright > 0)&&(endtimeBlockright< millis())){
    digitalWrite(pinBlockright,LOW);
    endtimeBlockright = 0;    
  };

// 
    if(((ser1&Drink) == Drink) && (endtimeDrink == 0)) { // если установлен бит Drink и время конца =0, то
      endtimeDrink = millis() + timeDrink;  // назнчачили момент выключения поилки
      digitalWrite(pinDrink,HIGH); // включили поилку
  }
  
*/
} // конец всего цикла
