import socket
import threading
import sys
import signal



HEADER = 4
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


DISCONNECT_MESSAGE = "!DISCONNECT"

instrucions_list = []
actuator_conn = None


clients = []

# Function to broadcast disconnect message
def broadcast_disconnect():
    print("\n[!] Sending 'Disconnect' to all clients...")
    for client in clients:
        try:
            client.sendall("DCNT\r".encode(FORMAT))
            client.close()
        except:
            pass

# Ctrl+C handler
def signal_handler(sig, frame):
    broadcast_disconnect()
    server.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

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
            print('PENEEE')
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
