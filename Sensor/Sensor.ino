#include "Sensor.h"

const uint16_t port = 5000;
const char *host = "192.168.70.163";
const char *SSID = "TECHLAB";
const char *password = "catolica11";

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
