import socket
import struct
import time
import sys

# RakNet protocol constants and utilities
RAKNET_MAGIC = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'

def send_packet(sock, ip, port, data):
    try:
        sock.sendto(data, (ip, port))
    except Exception as e:
        print(f"Error sending packet: {e}")

def recv_packet(sock):
    try:
        data, addr = sock.recvfrom(4096)
        print(f"Received {len(data)} bytes from {addr}: {data.hex()}")
        return data, addr
    except socket.timeout:
        return None, None

def build_unconnected_ping():
    # 0x01 | Timestamp (8 bytes) | Magic | Client GUID (8 bytes)
    timestamp = int(time.time() * 1000)
    client_guid = 0x123456789ABCDEF0
    return struct.pack('>BQ', 0x01, timestamp) + RAKNET_MAGIC + struct.pack('>Q', client_guid)

def build_unconnected_pong():
    # 0x1c | Timestamp (8 bytes) | Server GUID (8 bytes) | Magic | Server ID (8 bytes) | Server Name (string)
    timestamp = int(time.time() * 1000)
    server_guid = 0x123456789ABCDEF0
    server_id = 0x0F0E0D0C0B0A0908
    server_name = "RakNetServer;MCPE;Test;19132;0;1"
    return struct.pack('>BQ', 0x1c, timestamp) + struct.pack('>Q', server_guid) + RAKNET_MAGIC + struct.pack('>Q', server_id) + server_name.encode()

def build_open_connection_request_1():
    # 0x05 | Protocol version (1 byte) | Magic | MTU size (2 bytes)
    protocol_version = 10
    mtu_size = 1492
    return struct.pack('>BB', 0x05, protocol_version) + RAKNET_MAGIC + struct.pack('>H', mtu_size)

def build_open_connection_reply_1():
    # 0x06 | Magic | Server GUID (8 bytes) | Security (1 byte) | MTU size (2 bytes)
    server_guid = 0x123456789ABCDEF0
    security = 0
    mtu_size = 1492
    return struct.pack('>B', 0x06) + RAKNET_MAGIC + struct.pack('>Q', server_guid) + struct.pack('>B', security) + struct.pack('>H', mtu_size)

def build_open_connection_request_2(ip, port):
    # 0x07 | Magic | Server address | MTU size | Client GUID
    client_guid = 0x123456789ABCDEF0
    mtu_size = 1492
    ip_bytes = b''.join([bytes([int(x)]) for x in ip.split('.')])
    server_addr = b'\x04' + ip_bytes + struct.pack('>H', port)
    return struct.pack('>B', 0x07) + RAKNET_MAGIC + server_addr + struct.pack('>H', mtu_size) + struct.pack('>Q', client_guid)

def build_open_connection_reply_2(ip, port):
    # 0x08 | Magic | Server address | MTU size | Server GUID
    server_guid = 0x123456789ABCDEF0
    mtu_size = 1492
    ip_bytes = b''.join([bytes([int(x)]) for x in ip.split('.')])
    server_addr = b'\x04' + ip_bytes + struct.pack('>H', port)
    return struct.pack('>B', 0x08) + RAKNET_MAGIC + server_addr + struct.pack('>H', mtu_size) + struct.pack('>Q', server_guid)

def build_connection_request():
    # 0x09 | Client Timestamp (8 bytes) | Client GUID (8 bytes)
    timestamp = int(time.time() * 1000)
    client_guid = 0x123456789ABCDEF0
    return struct.pack('>BQ', 0x09, timestamp) + struct.pack('>Q', client_guid)

def build_connection_request_accepted(ip, port):
    # 0x10 | Server Timestamp (8 bytes) | Client Timestamp (8 bytes) | Server Addr | System Index (2) | Peer Addr List (empty)
    server_time = int(time.time() * 1000)
    client_time = int(time.time() * 1000)
    ip_bytes = b''.join([bytes([int(x)]) for x in ip.split('.')])
    server_addr = b'\x04' + ip_bytes + struct.pack('>H', port)
    system_index = 0
    return struct.pack('>BQQ', 0x10, server_time, client_time) + server_addr + struct.pack('>H', system_index)

def build_new_incoming_connection(ip, port):
    # 0x13 | Server Addr | System Index (2) | Peer Addr List (empty)
    ip_bytes = b''.join([bytes([int(x)]) for x in ip.split('.')])
    server_addr = b'\x04' + ip_bytes + struct.pack('>H', port)
    system_index = 0
    return struct.pack('>B', 0x13) + server_addr + struct.pack('>H', system_index)

def build_connected_ping():
    # 0x00 | Timestamp (8 bytes)
    timestamp = int(time.time() * 1000)
    return struct.pack('>BQ', 0x00, timestamp)

def build_connected_pong():
    # 0x03 | Timestamp (8 bytes)
    timestamp = int(time.time() * 1000)
    return struct.pack('>BQ', 0x03, timestamp)

def main():
    if len(sys.argv) < 5:
        print(f"Uso: python {sys.argv[0]} <ip> <puerto> <tiempo_segundos> <metodo>")
        print("Metodos: ping, pong, open1, reply1, open2, reply2, connreq, connaccept, newconn, cping, cpong, all")
        sys.exit(1)
    ip = sys.argv[1]
    port = int(sys.argv[2])
    duration = int(sys.argv[3])
    method = sys.argv[4].lower()

    # Build packet list for 'all' or single method
    packets = []
    if method == "all":
        packets = [
            build_unconnected_ping(),
            build_unconnected_pong(),
            build_open_connection_request_1(),
            build_open_connection_reply_1(),
            build_open_connection_request_2(ip, port),
            build_open_connection_reply_2(ip, port),
            build_connection_request(),
            build_connection_request_accepted(ip, port),
            build_new_incoming_connection(ip, port),
            build_connected_ping(),
            build_connected_pong()
        ]
        method_names = [
            "UnconnectedPing","UnconnectedPong","OpenConnReq1","OpenConnReply1","OpenConnReq2","OpenConnReply2",
            "ConnRequest","ConnRequestAccepted","NewIncomingConn","ConnectedPing","ConnectedPong"
        ]
    else:
        method_map = {
            'ping': build_unconnected_ping,
            'pong': build_unconnected_pong,
            'open1': build_open_connection_request_1,
            'reply1': build_open_connection_reply_1,
            'open2': lambda: build_open_connection_request_2(ip, port),
            'reply2': lambda: build_open_connection_reply_2(ip, port),
            'connreq': build_connection_request,
            'connaccept': lambda: build_connection_request_accepted(ip, port),
            'newconn': lambda: build_new_incoming_connection(ip, port),
            'cping': build_connected_ping,
            'cpong': build_connected_pong
        }
        if method not in method_map:
            print("Metodo no reconocido.")
            sys.exit(1)
        packets = [method_map[method]()]
        method_names = [method]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    end_time = time.time() + duration
    sent = 0

    print(f"Enviando paquetes '{', '.join(method_names)}' a {ip}:{port} durante {duration} segundos.")
    try:
        while time.time() < end_time:
            for idx, packet in enumerate(packets):
                send_packet(sock, ip, port, packet)
                sent += 1
                data, addr = recv_packet(sock)
                if data:
                    print(f"Respuesta a {method_names[idx]}: {data.hex()}")
            time.sleep(0.5)
    finally:
        sock.close()
        print(f"Paquetes enviados: {sent}")

if __name__ == "__main__":
    main()
