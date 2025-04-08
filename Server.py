import socket
import threading
import sys
import signal
import config


class Server:
    def __init__(self, host, port, sensor_config):
        self.addr = (host, port)
        self.sensor_config = sensor_config
        self.clients = []
        self.actuator_conn = None

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.addr)

        # Setup shutdown hook
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
                client.sendall(f"{config.DISCONNECT}\r".encode(config.FORMAT))
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
        return conn.recv(64).decode(config.FORMAT).strip()

    def route_message(self, conn, addr, msg):
        if msg.startswith(config.SENSOR_CONFIG):
            self.send_config_to_sensor(conn)
        elif msg.startswith(config.SENSOR_STATE):
            self.forward_sensor_state(msg)
        elif msg.startswith(config.ACTOR_STATE):
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
            conn.sendall(message.encode(config.FORMAT))
            print("[CONFIG] Sent sensor config")
        except Exception as e:
            print(f"[ERROR] Sending config: {e}")

    def forward_sensor_state(self, message):
        state = message.split('|')[1]
        print(state)
        if self.actuator_conn:
            try:
                
                self.actuator_conn.sendall(f"{state}\r".encode(config.FORMAT))
                print(f"[FORWARD] Sensor state '{state}' sent to actuator")
            except Exception as e:
                print(f"[ERROR] Forwarding state: {e}")
        else:
            print("[WARN] No actuator connected")


if __name__ == "__main__":
    config = "00,10;10,20;20,30"
    host = "192.168.70.163"
    port = 5000
    server_instance = Server(host, port , config)
    print("[STARTING] Server is starting...")
    server_instance.start()