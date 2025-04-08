#include <string>
#include "HardwareSerial.h"
#include "../RemoteClient.h"
#include "../WifiManager.h"
#include "UltraSonicSensor.h"

class Sensor{
  private:
    WifiManager wifiManager;
    RemoteClient client;
    UltraSonicSensor sensor;
    byte ranges[6];
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
      requestConfig("SSRC");
      delay(1000);
    }
    
    void getRanges(String config){
      for(int i = 0; i < 6; i++)
        ranges[i] = (config.substring(i * 3, 2 + (i * 3))).toInt();
    }

    void requestConfig(String msg){
      client.sendMessage(msg);
      delay(500);
      String config = client.readMessage();
      getRanges(config);
    }

    float readDistance(){
      sensor.update();
      return sensor.getDistanceCM();
    }

    byte classifyDistance(){
      byte state = 3;
      float distance = readDistance();
      
      if(distance >= ranges[0] && distance < ranges[1]) state = 0;
      else if(distance >= ranges[2] && distance < ranges[3]) state = 1;
      else if(distance >= ranges[4] && distance < ranges[5]) state = 2;

      return state;
    }

    void sendState(){
      byte state = classifyDistance();
      if(currentState != state){
        client.sendMessage("SSRS|" + String(state) + "\r");
        currentState = state;
      } 
    }

    void update(){
      if(!client.isConnected()){
        Serial.println("Reconnecting...");
        delay(5000);
        client.connectToServer();
        requestConfig("SSRC");
      } else {
        if (client.readMessage() != "DCNT"){
          sendState();
          delay(500);
        } 
        else{
          client.disconnect();
        }
      }
    }
};