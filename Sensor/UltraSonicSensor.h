#ifndef _ULTRASONICSENSOR_H_
#define _ULTRASONICSENSOR_H_

class UltraSonicSensor {
  private:
    byte triggerPin;
    byte echoPin;
    float distance;
  public:
    UltraSonicSensor(const byte& triggerPin, const byte& echoPin):
    triggerPin(triggerPin), echoPin(echoPin), distance(0)  
    {
        		
    }
    ~UltraSonicSensor(){}

    void update()            
    {
      pinMode(triggerPin, OUTPUT);
      digitalWrite(triggerPin, LOW);
      delayMicroseconds(2);
      digitalWrite(triggerPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(triggerPin, LOW);
      pinMode(echoPin, INPUT);
      this->distance = pulseIn(echoPin, HIGH); 
    }
    float getDistanceCM() const 
    {       
      return (0.01723 * this->distance);
    }
    float getDistanceINCH() const 
    {
      return (getDistanceCM() / 2.54);
    }   
};


#endif // _ULTRASONICSENSOR_H_

