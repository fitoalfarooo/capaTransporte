import shutil
import socket
import threading
import os
from datetime import datetime
import json

HEADER = 64
PORT = int(os.environ.get("PORT", 5050))
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def _input(conn, addr):

    try:
        print("\n[*] NUEVO CLIENTE CONECTADO.")
        print(f"[+] IP SOCKET: {addr[1]}")
        print(f"[+] IP CLIENTE: {addr[0]}")
        print(f"[+] IP SERVER: {SERVER}")
        print(f"[+] PUERTO: {PORT}")

        res = conn.recv(BUFFER_SIZE).decode(FORMAT)

        header = json.loads(res)

        conn.send(bytes("ESPERANDO AL SERVIDOR...", FORMAT))

        threading.current_thread().setName(header['input_name'])
        filesize = int(header['filesize'])

        os.makedirs("PETICIONES")
        input_file = f"PETICIONES/nuevaPeticion{header['input_extension']}"
        print(f"\n[*] NUEVA PETICION: {input_file}")
        output_file = f"PETICIONES/respuestaPeticion{header['output_extension']}"
        print(f"[*] NUEVA RESPUESTA: {output_file}")

        print(f"[+] RECIBIENDO... {input_file}")
        with open(input_file, "wb") as file:
            data = 0
            while data < filesize:
                bytes_read = conn.recv(BUFFER_SIZE)
                file.write(bytes_read)
                data += len(bytes_read)
            file.close()

        print(f"[+] ARCHIVO {input_file} RECIBIDO EXITOSAMENTE.")

        fullDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("\n[*] INICIO CONVERSION:", fullDate)

        #ffmpeg.input(input_file).output(output_file).run(capture_stdout=False, capture_stderr=True,
        #                                                 overwrite_output=True)
        size = os.path.getsize(input_file)
        conn.send(bytes(f"True{SEPARATOR}{size}", FORMAT))

        with open(input_file, "rb") as file:
            bytes_read = file.read(BUFFER_SIZE)
            while bytes_read:
                conn.sendall(bytes_read)
                bytes_read = file.read(BUFFER_SIZE)
            file.close()

        fullDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("[*] FIN CONVERSION:", fullDate)
        print('\n[*] PETICION FINALIZADA EXITOSAMENTE.')
        conn.close()

    except Exception as e:
        print(f"\n[*] ERROR: {e}")
        conn.close()

    finally:
        if os.path.isdir(f"./PETICIONES"):
            shutil.rmtree(f"./PETICIONES")
            print('[*] CARPETA DE PETICIONES ELIMINADA')

def start():
    try:

        server.listen()
        print(f"[*] SERVIDOR ESCUCHANDO EN {SERVER}:{PORT}")
        fullDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("[+] FECHA Y HORA ACTUAL DEL SERVIDOR:", fullDate)
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=_input, args=(conn, addr,))
            thread.start()
            print(f"[*] CONEXIONES ACTIVAS: {threading.activeCount() - 1}")

    except Exception as e:
        print(f"\n[*] ERROR: {e}")

print("\n[INICIANDO] el servidor esta arrancando...")
start()