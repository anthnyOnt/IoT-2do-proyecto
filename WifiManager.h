#include "WiFiMulti.h";

class WifiManager {
  private:
    WiFiMulti wifiMulti;
    unsigned long connectionTimeout;
  
  public:
    WifiManager(unsigned long connectionTimeout = 30000) : connectionTimeout(connectionTimeout) {}

    void addNetwork(const char* ssid, const char* password) {
      wifiMulti.addAP(ssid, password);
    }
    
    bool connect() {
      unsigned long startAttemptTime = millis();
      Serial.print("Connecting to WiFi...");

      while (wifiMulti.run() != WL_CONNECTED) {
        if (millis() - startAttemptTime >= connectionTimeout) {
          Serial.println("Connection timeout.");
          return false;  
        }
        delay(500);
        Serial.print(".");
      }

      Serial.println("Connected to Wi-Fi!");
      return true;
    }

    bool isConnected() {
      return WiFi.isConnected();
    }

    void printIPAddress() {
      if (isConnected()) {
        Serial.print("IP Address: ");
        Serial.println(WiFi.localIP());
      } else {
        Serial.println("Not connected to Wi-Fi.");
      }
    }
};