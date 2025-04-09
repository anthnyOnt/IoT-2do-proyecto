#include "Sensor.h"
#include "../config.h"

// const uint16_t port = 1234;
// const char *host = "x.x.x.x";
// const char *SSID = "network";
// const char *password = "password";

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
