#include "WiFi.h";

class RemoteClient {
  private:
    WiFiClient client;
    const char* host;
    uint16_t port;
  
  public:
    RemoteClient(const char* host, uint16_t port) : host(host), port(port) {}

    bool connectToServer() {
      Serial.print("Connecting to ");
      Serial.print(host);
      Serial.println("...");

      if(client.connect(host,port)){
        Serial.println("Connected to server");
        return true;
      } else {
        Serial.println("Connection failed");
        return false;
      }
    }

    void sendMessage(String message) {
      if (client.connected()) {
        client.print(message);
        Serial.println("Sent: " + message); 
      } else {
        Serial.println("Not connected. Can't send message.");
      }
    }

    String readMessage() {
      String message = "";

      if (client.available() > 0) {
        message = client.readStringUntil('\r');
        Serial.print("Received: ");
        Serial.println(message);
      } else {
        Serial.println("No data available.");
      }
      return message;
    }

    bool isConnected(){
      return client.connected();
    }

    void disconnect() {
      client.stop();
      Serial.println("Disconnected from server.");
    }
};