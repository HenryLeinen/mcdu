from mcdu.avionics import Avionics

import threading
import socket
import struct

class XPlaneReceiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2)

        self.avionics = Avionics()
        self.active = True

    def run(self):
        self.sock.bind(("", 49003))

        while self.active:
            try:
                data, addr = self.sock.recvfrom(1024)
                self.parse(data)
            except socket.timeout:
                pass

    def stop(self):
        self.active = False
        self.sock.close()

    def parse(self, data):
        header = struct.unpack("5s", data[:5])
        data = data[5:]

        update = {}

        for i in range(0, len(data), 36):
            packet = struct.unpack("i8f", data[i:i+36])

            if packet[0] == 3:
                update["speed"] = int(round(packet[4]))
            elif packet[0] == 5:
                wind_heading = int(round(packet[5]))
                wind_speed = int(round(packet[4]))
                update["wind"] = "%i/%i" % (wind_heading, wind_speed)
            elif packet[0] == 6:
                update["temp"] = int(round(packet[2]))
            elif packet[0] == 14:
                update["gear"] = True if packet[1] > 0.1 else False
                update["brk"] = True if packet[2] > 0.1 else False
            elif packet[0] == 17:
                update["hdg"] = int(round(packet[3]))
            elif packet[0] == 20:
                update["pos"] = (round(packet[1], 8), round(packet[2], 8))
                update["alt"] = int(round(packet[3]))
            elif packet[0] == 37:
                update["eng"] = (packet[1], packet[2], packet[3], packet[4])

        self.avionics.update(update)
