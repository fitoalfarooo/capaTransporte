import os
import socket
import json

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
FORMAT = "utf-8"
ADDR = ("", 0)

videoFormats = [".mp4",".mkv",".rawvideo",".webm",".mov"]
audioFormats = [".mp3",".flac",".wav",".aac"]

try:
    print("\n[Ejemplo de parametros]"
          "\ninput = C:\\Users\\warner\\Desktop\\tareaRedes\\video.mp4" +
          "\noutput = C:\\Users\\warner\\Desktop\\tareaRedes\\respuesta.mkv" +
          "\nhost = 192.168.1.186"
          "\nport = 5050\n")

    input_file = input("Digite el nombre del archivo a convertir [input]: ")
    output_file = input("Digite el nombre del archivo de salida [output]: ")
    host = input("Digite la direccion del servidor [host]: ")
    port = int(input("Digite el numero de puerto [port]: "))
    ADDR = (host, port)

    filesize = os.path.getsize(input_file)
    input_name, input_extension = os.path.splitext(input_file)
    output_name, output_extension = os.path.splitext(output_file)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\n[+] CONECTANDO A {host}:{port}")
    client.connect(ADDR)
    print("[*] CONECTADO.")

    data = {
        "input_name": input_name,
        "input_extension": input_extension,
        "output_name": output_name,
        "output_extension": output_extension,
        "filesize": filesize
    }

    json_response = bytes(json.dumps(data), FORMAT)
    client.sendall(json_response)

    res = client.recv(BUFFER_SIZE).decode(FORMAT)

    print(f"\n[*] ENVIANDO {input_file}...")

    with open(input_file, "rb") as file:
        bytes_read = file.read(BUFFER_SIZE)
        while bytes_read:
            client.sendall(bytes_read)
            bytes_read = file.read(BUFFER_SIZE)
        file.close()

    print(f"[*] {input_file} ENVIADO EXITOSAMENTE. ")
    print("\n[+] ESPERANDO RESPUESTA DEL SERVIDOR. ")
    res = client.recv(BUFFER_SIZE).decode(FORMAT)
    status, size = res.split(SEPARATOR)
    size = int(size)

    print(f"[*] RESPUESTA: Status: {status} / size: {size}")
    print("\n[*] TRANSFORMANDO RESPUESTA.... ")
    if status:
        with open(output_file, "wb") as file:
            data = 0
            while data < size:
                bytes_read = client.recv(BUFFER_SIZE)
                file.write(bytes_read)
                data += len(bytes_read)
            file.close()
        print("[*] RESPUESTA OBTENIDA EXITOSAMENTE. ")
    print("[FIN]")
    client.close()

except Exception as e:
    print(f"\n[*] ERROR: {e}")