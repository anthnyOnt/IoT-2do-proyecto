import socket
import threading
import sys
import signal
import time

#ADDRESS
PORT = 5000
SERVER = "192.168.0.8"
ADDR = (SERVER, PORT)

#MISC
FORMAT = "utf-8"

#MESSAGES
SENSOR_CONFIG = "SSRC" #SSRC (client -> server) request sensor config, ranges and states (server -> client) SSRC|0,10;10,20;20,30\r sends ranges
SENSOR_STATE= "SSRS" #SSRS|2\r (client -> server) sensor stores or sends the value to the actuator (server -> actuator) ACTR|0,1;1,0;2,0\r
ACTOR_STATE = "ACTS" # (server -> client) server tells which leds are turned on or off
DELIMITER = "|"
DISCONNECT = "DCNT"
CHECK_CONNECTION = "CHCK"

CONFIG = "00,20;20,40;40,60"

class Server:
    def __init__(self, host, port, sensor_config):
        self.addr = (host, port)
        self.sensor_config = sensor_config
        self.clients = []
        self.actuator_conn = None
        self.sensor_conn = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.addr)
        self.format = FORMAT

        signal.signal(signal.SIGINT, self.shutdown_handler)

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.addr}")

        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def shutdown_handler(self, sig, frame):
        print("\n[!] Shutting down server...")
        self.broadcast_disconnect()
        self.server.close()
        sys.exit(0)

    def broadcast_disconnect(self):
        for client in self.clients:
            try:
                client.sendall(f"{DISCONNECT}\r".encode(self.format))
                client.close()
                print("[DISCONNECT] Client disconnected")
            except:
                pass

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        self.clients.append(conn)

        with conn:
            while True:
                try:
                    msg = self.receive_message(conn)
                    if not msg:
                        break
                    self.route_message(conn, addr, msg)
                except Exception as e:
                    print(f"[ERROR] From {addr}: {e}")
                    break
                
    def receive_message(self, conn):
        return conn.recv(64).decode(FORMAT).strip()

    def route_message(self, conn, addr, msg):
        if msg.startswith(SENSOR_CONFIG):
            self.send_config_to_sensor(conn)
        elif msg.startswith(SENSOR_STATE):
            self.forward_sensor_state(msg)
        elif msg.startswith(ACTOR_STATE):
            self.register_actuator(conn)
        else:
            self.handle_unknown_message(addr, msg)

    def register_actuator(self, conn):
        self.actuator_conn = conn
        print("[INFO] Actuator registered")

    def handle_unknown_message(self, addr, msg):
        print(f"[UNKNOWN] Message from {addr}: {msg}")


    def send_config_to_sensor(self, conn):
        try:
            message = f"{self.sensor_config}\r"
            conn.sendall(message.encode(self.format))
            print("[CONFIG] Sent sensor config")
        except Exception as e:
            print(f"[ERROR] Sending config: {e}")

    def forward_sensor_state(self, message):
        state = message.split('|')[1]
        print(state)
        if self.actuator_conn:
            try:
                
                self.actuator_conn.sendall(f"{state}\r".encode(self.format))
                print(f"[FORWARD] Sensor state '{state}' sent to actuator")
            except Exception as e:
                print(f"[ERROR] Forwarding state: {e}")
        else:
            print("[WARN] No actuator connected")

if __name__ == "__main__":
    server_instance = Server(SERVER, PORT ,CONFIG)
    print("[STARTING] Server is starting...")
    server_instance.start()