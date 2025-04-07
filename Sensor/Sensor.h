#include "../RemoteClient.h"
#include "../WifiManager.h"
#include "UltraSonicSensor.h"

class Sensor{
  private:
    WifiManager wifiManager;
    RemoteClient client;
    UltraSonicSensor sensor;
    byte currentState;

  public:
    Sensor(byte triggerPin, byte echoPin, const char* SSID, const char* password, const char* host, const uint16_t& port)
    : sensor(triggerPin, echoPin), client(host, port), currentState(-1){
      wifiManager.addNetwork(SSID, password);
    }

    void init(){
      Serial.begin(115200);
      wifiManager.connect();
      client.connectToServer();
      delay(1000);
    }
    
    float readDistance(){
      sensor.update();
      return sensor.getDistanceCM();
    }

    byte getState(){
      byte state = 3;
      float distance = readDistance();
      
      if(distance < 20) state = 0;
      else if(distance >= 20 && distance < 40) state = 1;
      else if(distance >= 40 && distance < 60) state = 2;

      return state;
    }

    void sendState(){
      byte state = getState();
      if(currentState != state){
        client.sendMessage("SNSR" + String(state));
        currentState = state;
      } 
    }

    void update(){
      if(!client.isConnected()){
        Serial.println("Reconnecting...");
        delay(5000);
        client.connectToServer();
      } else {
        sendState();
        delay(500);
      }
    }
};