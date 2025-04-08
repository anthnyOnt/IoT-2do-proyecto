import socket
import threading
import sys
import signal



HEADER = 4
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"




#ACTR|2|\r


#headers
SENSOR_CONFIG = "SSRC" #SSRC (client -> server) request sensor config, ranges and states (server -> client) SSRC|0,0,10;1,10,20;2,20,30\r sends ranges and states
SENSOR_STATE= "SSRS" #SSRS|2\r (client -> server) sensor stores or sends the value to the actuator 
ACTOR_CONFIG = "ACTC" #ACTC (client -> server) request actuator states, same as sensor states (server -> client) ACTC|0;1;2\r sends states
ACTOR_STATE = "ACTS" #ACTR|0,1;1,0;2,0\r (server -> client) server tells which leds are turned on or off

DELIMITER = "|"
DISCONNECT = "DCNT"

states = [0,1,2]
min_range = (0,15)
mid_range = (15,30)
max_range = (30,45)

range_settings = {
    states[0]: min_range,
    states[1]: mid_range,
    states[2]: max_range
}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

instrucions_list = []
actuator_conn = None


clients = []

# Function to broadcast disconnect message
def broadcast_disconnect():
    print("\n[!] Sending 'Disconnect' to all clients...")
    for client in clients:
        try:
            client.sendall(f"{DISCONNECT}\r".encode(FORMAT))
            client.close()
            print("Disconnected")
        except:
            pass

# Ctrl+C handler
def signal_handler(sig, frame):
    broadcast_disconnect()
    server.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



def send_sensor_config():
    pass

def send_actuator_config():
    pass

def handle_requests(protocol):
    if (protocol == SENSOR_CONFIG):
        send_sensor_config()
    elif (protocol == ACTOR_CONFIG):
        send_actuator_config()



def handle_sensor(conn):
    clients.append(conn)
    print("[SENSOR CONNECTED]")
    try:
        while True:
            msg = conn.recv(1).decode(FORMAT)
            if not msg:
                break
            print(f"[SENSOR]: {msg}")
            if actuator_conn:
                try:
                    actuator_conn.sendall(f"{msg}\r".encode(FORMAT))
                except:
                    print("[!] Failed to push to actuator")
    finally:
        print("[SENSOR DISCONNECTED]")
        clients.remove(conn)
        conn.close()

def handle_actuator(conn):
    global actuator_conn
    actuator_conn = conn
    clients.append(conn)
    print(f"[ACTUATOR CONNECTED]")
    try:
        while True:
            pass
    finally:
        print("[ACTUATOR DISCONNECTED]")
        clients.remove(conn)
        conn.close()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    hdr = conn.recv(HEADER).decode(FORMAT)
    try:
        if hdr == "SNSR":
            handle_sensor(conn)
        elif hdr == "ACTR":
            handle_actuator(conn)
        else:
            conn.close()
    except Exception as e:
        print(f"[ERROR] {e}")
        conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start()
