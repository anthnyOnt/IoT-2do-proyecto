#include "Sensor.h"

const uint16_t port = 5000;
const char *host = "192.168.0.8";
const char *SSID = "Ontiveros SRL";
const char *password = "376098029";

const byte triggerPin = 26;
const byte echoPin = 25;

Sensor s(triggerPin, echoPin, SSID, password, host, port);

void setup()
{
  s.init();
}

void loop()
{
  s.update();
}
