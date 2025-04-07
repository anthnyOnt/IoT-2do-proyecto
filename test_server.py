import socket
import threading



HEADER = 4
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, PORT)
server.bind(ADDR)
FORMAT = "utf-8"

DISCONNECT_MESSAGE = "!DISCONNECT"

instrucions_list = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        hdr = conn.recv(HEADER).decode(FORMAT)
        if hdr:
            if hdr == "ACTR":
                if instrucions_list:
                    conn.sendall(str(instrucions_list.pop(0) + "\r").encode(FORMAT))
            elif hdr == "SNSR":
                instruction = conn.recv(1).decode(FORMAT)
                instrucions_list.append(instruction)
                print(f"[SENSOR]: {instruction}")
                print(instrucions_list)


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")




print("[STARTING] Server is starting...")
start()
