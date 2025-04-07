#include "Actuator.h"

const uint16_t port = 5000;
const char *host = "192.168.0.8";
const char *SSID = "NETWORK";
const char *password = "PASSWORD";

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