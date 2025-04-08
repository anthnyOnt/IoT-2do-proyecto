#include <Arduino.h>

class Led {

private:
  byte pin;
  bool isOn = false;

public:
  const static byte STATE_OFF = 0;
  const static byte STATE_ON = 1;   

public:
  Led(byte pin) : pin(pin){
    pinMode(pin, OUTPUT);
    turnOff();
  }

  void setState(bool state){
    digitalWrite(pin, state);
    isOn = state;
  }

  byte getPin(){
    return pin;
  }
  void turnOn(){
    digitalWrite(pin, HIGH);
    isOn = true;
  }
  void turnOff(){
    digitalWrite(pin, LOW);
    isOn = false;
  }
};

