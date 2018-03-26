from mcdu.avionics import Avionics
import threading, pyuipc, time

class FSXReceiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.avionics = Avionics()
        self.active = True
        self.connected = False

        self.pdata = pyuipc.prepare_data([
           (0x6010, "f"),
           (0x6018, "f"),
           (0x6020, "f"),
           (0x6030, "f"),
           (0x6040, "f"),
           (0x2de0, "f"),
           (0x2de8, "f"),
           (0x0e8c, "h"),
           (0x0bc8, "H"),
           (0x0be8, "u"),
           (0x0896, "H"),
           (0x092e, "H"),
           (0x09c6, "H"),
           (0x0a5e, "H"),
        ], True)

    def run(self):
        while self.active:
            if not self.connected:
                self.connected = self.connect()
                time.sleep(2)
                continue

            print("connected to fsx!")
            self.read()
            time.sleep(5)

    def connect(self):
        try:
            pyuipc.open(pyuipc.SIM_FSX)
        except pyuipc.FSUIPCException:
            return False
        else:
            return True

    def read(self):
        try:
            data = pyuipc.read(self.pdata)
        except pyuipc.FSUIPCException:
            self.connected = False
            return

        wind_heading = int(round(data[5]))
        wind_speed = int(round(data[6]))

        update = {
            "pos": (round(data[0], 8), round(data[1], 8)),
            "alt": int(round(data[2]*3.28)), # m to ft
            "speed": int(round(data[3]*1.944)), # m/s to kt
            "hdg": int(round(data[4]*57.296))%360, # rad to deg
            "wind": "%i/%i" % (wind_heading, wind_speed),
            "temp": data[7]/256,
            "brk": data[8] == 32767,
            "gear": data[9] == 16383,
            "eng": (round(data[10]/163.84, 1),
                    round(data[11]/163.84, 1),
                    round(data[12]/163.84, 1),
                    round(data[13]/163.84, 1)),
        }

        print(update)

        self.avionics.update(update)

    def stop(self):
        self.active = False
        pyuipc.close()
