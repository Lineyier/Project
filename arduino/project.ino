#include <Temperature_LM75_Derived.h>
#include <GyverBME280.h>
#include <DHT22.h>
#include <Adafruit_Sensor.h>
#include <SoftwareSerial.h>
//define pin data
#define pinDATA 2 // SDA, or almost any other I/O pin


Generic_LM75 temperature;
GyverBME280 bmp;
DHT22 dht22(pinDATA); 


void setup() {
  while(!Serial) {}
  
  Serial.begin(9600);
  Serial1.begin(38400);   // Установка скорости передачи для порта 1 (RX1,TX1) от Arduino к HC-05
  if (!bmp.begin()) Serial.println("BMP error!");  
  Wire.begin();
  //Serial.begin(9600);     // Установка скорости передачи для порта 0 (USB) от Arduino к ПК
  
  delay(4000);
}

void loop() {
  //if (Serial1.available()) {  // если пришли данные с порта 1 (RX1,TX1)
   // char c = Serial1.read(); // читаем из порта 1 (RX1,TX1)
  //  Serial.print(c);         // пишем в порт 0 (USB)
 // }
  if (Serial.available()) { // если пришли данные с порта 0 (USB)
    char c = Serial.read(); // читаем из hardware-порта
    Serial.print(c);        // пишем в hardware-порт
    Serial1.write(c);       // пишем в software-порт
  }

     // LM75
  // Температура
  Serial1.print("LM75 ");
  Serial1.print(temperature.readTemperatureC());
  Serial1.println("C ");
  //}
  delay(10);
    // DHT22
  // Влажность
  float h = dht22.getHumidity();
  Serial1.print("DHT22 ");
  Serial1.print(h);
  Serial1.println("% ");
  delay(10);
  // BMP280
  // Давление
  Serial1.print("BMP280 ");
  Serial1.print((bmp.readPressure()/133.322368));
  Serial1.println(" mm.Hg. ");

  
  delay(2000);
}
