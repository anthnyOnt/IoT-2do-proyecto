#include "Sensor.h"
#include "../config.h"

// const uint16_t port = 1234;
// const char *host = "x.x.x.x";
// const char *SSID = "network";
// const char *password = "password";

const byte triggerPin = 26;
const byte echoPin = 25;

Sensor sensor(triggerPin, echoPin, SSID, password, host, port);

void setup()
{
  sensor.init();
}

void loop()
{
  sensor.update();
}
