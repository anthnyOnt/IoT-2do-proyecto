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
SENSOR_CONFIG = "SSRC" #SSRC (client -> server) request sensor config, ranges and states (server -> client) SSRC|0,10;10,20;20,30\r sends ranges
SENSOR_STATE= "SSRS" #SSRS|2\r (client -> server) sensor stores or sends the value to the actuator (server -> actuator) ACTR|0,1;1,0;2,0\r
ACTOR_STATE = "ACTS" # (server -> client) server tells which leds are turned on or off

DELIMITER = "|"
DISCONNECT = "DCNT"


config = "15,30;30,45;45,60"

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



def send_sensor_config(conn):
    message = f"{config}\r"
    conn.sendall(message.encode(FORMAT))


def send_sensor_state(state):
    if actuator_conn:
        state = state.split('|')[1]
        print(f"STATE: {state}")
        message = ""
        if (state == '0'):
            message = "0,1;1,0;2,0"
        elif (state == '1'):
            message = "0,0;1,1;2,0"
        elif (state == '2'):
            message = "0,0;1,0;2,1"
        else:
            message = "0,0;1,0;2,0"
        actuator_conn.sendall(f"{message}\r".encode(FORMAT))
    else:
        print("THERE IS NO ACTUATOR")


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        while True:
            try:
                message = conn.recv(64).decode(FORMAT).strip()
                if not message:
                    break
                if message.startswith(SENSOR_CONFIG):
                    send_sensor_config(conn)
                elif message.startswith(SENSOR_STATE):
                    send_sensor_state(message)
                elif message.startswith(ACTOR_STATE):
                    global actuator_conn
                    actuator_conn = conn
                else:
                    print("UNKNOWN REQUEST")
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
