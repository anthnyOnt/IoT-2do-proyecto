#include <cstdlib>
#include "../RemoteClient.h"
#include "../WifiManager.h"
#include "Led.h"

class Actuator{
  private:
    WifiManager wifiManager;
    RemoteClient client;
    Led redLed;
    Led yellowLed;
    Led greenLed;
    byte currentLed;

  public:
    Actuator(byte greenLed, byte yellowLed, byte redLed, const char* SSID, const char* password, const char* host, const uint16_t& port) 
    : greenLed(greenLed), yellowLed(yellowLed), redLed(redLed), client(host, port), currentLed(3){ //
      wifiManager.addNetwork(SSID, password);
    }

    void init(){
      Serial.begin(115200);
      wifiManager.connect();
      client.connectToServer();
      client.sendMessage("ACTS");
      delay(1000);
    }

    void readInstructions(){
      String instruction = client.readMessage();
      if(instruction == "DCNT"){
        currentLed = 3;
        client.disconnect();
        
      } else if (instruction != ""){
        currentLed = instruction.toInt();
      }
      turnOn();
    }

    void turnOn(){
      redLed.setState(currentLed == 0 ? Led::STATE_ON : Led::STATE_OFF);
      yellowLed.setState(currentLed == 1 ? Led::STATE_ON : Led::STATE_OFF);
      greenLed.setState(currentLed == 2 ? Led::STATE_ON : Led::STATE_OFF);
    }

    void update(){
      if(!client.isConnected()){
        Serial.println("Reconnecting...");
        delay(5000);
        client.connectToServer();
        client.sendMessage("ACTS");
      } else {
        readInstructions();
        delay(500);
      }
    }    
};