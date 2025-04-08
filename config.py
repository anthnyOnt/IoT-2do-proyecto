#ADDRESS
PORT = 5000
SERVER = "192.168.105.215"
ADDR = (SERVER, PORT)

#MISC
FORMAT = "utf-8"

#MESSAGES
SENSOR_CONFIG = "SSRC" #SSRC (client -> server) request sensor config, ranges and states (server -> client) SSRC|0,10;10,20;20,30\r sends ranges
SENSOR_STATE= "SSRS" #SSRS|2\r (client -> server) sensor stores or sends the value to the actuator (server -> actuator) ACTR|0,1;1,0;2,0\r
ACTOR_STATE = "ACTS" # (server -> client) server tells which leds are turned on or off
DELIMITER = "|"
DISCONNECT = "DCNT"