#include <cstdlib>
#include "../RemoteClient.h"
#include "../WifiManager.h"
#include "Led.h"

class Actuator{
  private:
    WifiManager wifiManager;
    RemoteClient client;
    Led leds[3];
    byte currentLed;

  public:
    Actuator(byte greenLed, byte yellowLed, byte redLed, const char* SSID, const char* password, const char* host, const uint16_t& port) 
    : client(host, port), currentLed(3){ //greenLed(greenLed), yellowLed(yellowLed), redLed(redLed),
      wifiManager.addNetwork(SSID, password);
      Led[0](redLed);
      Led[1]](yellowLed);
      Led[2](greenLed);
    }

    void init(){
      Serial.begin(115200);
      wifiManager.connect();
      client.connectToServer();
      delay(1000);
      client.sendMessage("ACTS");
    }

    String getInstruction(){
      String instruction = client.readMessage();
      if(instruction == "DCNT"){
        currentLed = 3;
        client.disconnect();
        return "";
      }
      return instruction;
    }

    void turnOn(byte leds[], byte values[]){
      this->leds[leds[0]].setState(values[0]);
      this->leds[leds[1]].setState(values[1]);
      this->leds[leds[2]].setState(values[2]);
      // redLed.setState(currentLed == 0 ? Led::STATE_ON : Led::STATE_OFF);
      // yellowLed.setState(currentLed == 1 ? Led::STATE_ON : Led::STATE_OFF);
      // greenLed.setState(currentLed == 2 ? Led::STATE_ON : Led::STATE_OFF);
    }

    void readInstructions(){
      String instruction = getInstruction();
      byte leds[3];
      byte values [3];
      for(int i = 0; i < 3; i++){
        leds[i] = (instruction.substring(i * 4, 1 + i * 4)).toInt();
        values[i] = (instruction.substring(2 + i * 4, 3 + i * 4)).toInt();
      }
      turnOn(leds, values);
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