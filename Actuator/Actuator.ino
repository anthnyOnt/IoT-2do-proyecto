#include "Actuator.h"

const uint16_t port = 5000;
const char *host = "192.168.70.163";
const char *SSID = "TECHLAB";
const char *password = "catolica11";

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