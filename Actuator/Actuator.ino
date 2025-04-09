#include "Actuator.h"
#include "../config.h"

// const uint16_t port = 1234;
// const char *host = "x.x.x.x";
// const char *SSID = "network";
// const char *password = "password";

const byte redLed = 25;
const byte yellowLed = 26;
const byte greenLed = 27;

Actuator a(greenLed, yellowLed, redLed, SSID, password, host, port);

void setup()
{
  a.init();
}

void loop()
{
  a.update();
}